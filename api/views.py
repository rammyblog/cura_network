import requests
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import serializers
from requests.exceptions import ConnectionError


from .models import HotelBooking
from .serializers import HotelBookingSerializer, HotelSerializer
from .utlis import load_and_dump_data


class API_Root(views.APIView):
    ''' List of all endpoints'''
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return Response({
            'list_properties': reverse('list_hotels', request=request, format=format),
            'create_booking': reverse('create_booking', request=request, format=format),
        })


class ListHotels(views.APIView):
    """
    View to list all hotels in a given area.

    * Requires the cordinates of the area i.e Longitude and Langtitude.
    * 
    """

    @swagger_auto_schema(
        responses={404: "You need to include the at in the params i.e '&at=42.36399,-71.05493' "}, manual_parameters=[
            openapi.Parameter('at', openapi.IN_QUERY, "LAT,LONG", type=openapi.TYPE_STRING, required=True),
        ],
    )
    def get(self, request):
        """
        Return a list of all hotels in a given area.

        * Requires LAT,LONG of the area as params
        * i.e https://curanetwork.herokuapp.com/api/properties?at=LAT,LONG
        * i.e at=42.36399,-71.05493
        * i.e https://curanetwork.herokuapp.com/api/properties?at=42.36399,-71.05493

        """
        try:
            cordinates = request.GET['at']

            if len(cordinates.split(',')) != 2:
                return Response(
                    'You need to input both the Latitude and Longitude', status=status.HTTP_400_BAD_REQUEST)

            base_url = 'https://discover.search.hereapi.com/v1/discover?q=hotels'
            params = dict(at=cordinates, apiKey=settings.HERE_API_KEY)

            try:
                is_cached = request.session['cordinates'] == cordinates
            except KeyError:
                is_cached = False
                request.session['cordinates'] = cordinates

            if not is_cached:
                try:
                    response = requests.get(base_url, params=params).json()
                except ConnectionError:
                    raise serializers.ValidationError('Your internet seems to be very slow or bad')
                request.session['hotels_data'] = response
                request.session['cordinates'] = cordinates

            hotels_data = request.session['hotels_data']

        except MultiValueDictKeyError:
            return Response("You need to include the at in the params i.e '&at=42.36399,-71.05493' ",
                            status=status.HTTP_400_BAD_REQUEST)

        context = dict(message='success', data=hotels_data)
        return Response(context, status=status.HTTP_200_OK)


class HotelBookingsCreate(views.APIView):
    """
          Create an hotel booking using the property ID from HERE places.

          * i.e here:pds:place:276u0vhj-b0bace6448ae4b0fbc1d5e323998a7d2

    """

    serializer_class = HotelBookingSerializer

    @staticmethod
    def get_hotel(request, property_id):
        base_url = 'https://lookup.search.hereapi.com/v1/lookup'
        params = dict(id=property_id, apiKey=settings.HERE_API_KEY)

        try:
            is_cached = request.session['property_id'] == property_id
        except KeyError:
            is_cached = False
            request.session['property_id'] = property_id

        if not is_cached:
            try:
                response = requests.get(base_url, params=params).json()
            except ConnectionError:
                raise serializers.ValidationError('Your internet seems to be very slow or bad')
            try:
                response['status'] = 404
                raise serializers.ValidationError('Wrong Property ID given')
            except KeyError:
                request.session['hotel_data'] = response
                request.session['property_id'] = property_id

        hotel_data = request.session['hotel_data']

        return hotel_data

    @staticmethod
    def get_hotel_data_dict(hotel_data):
        hotel_title = hotel_data['title']
        property_id = hotel_data['id']
        postal_code = hotel_data['address']['postalCode']
        latitude = hotel_data['position']['lat']
        longitude = hotel_data['position']['lng']

        request_data = dict(property_name=hotel_title, property_id=property_id, postal_code=postal_code,
                            latitude=latitude, longitude=longitude)

        return request_data

    @swagger_auto_schema(
        responses={200: HotelSerializer(many=True), 400: "You need to include the property_id in the request body i.e "
                                                         "'here:pds:place:276u0vhj-b0bace6448ae4b0fbc1d5e323998a7d2' "},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['property_id'],
            properties={
                'property_id': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ), )
    def post(self, request, *args, **kwargs):
        try:
            property_id = request.data['property_id']
        except MultiValueDictKeyError:
            return Response(
                "You need to include the property_id in the request body i.e "
                "'here:pds:place:276u0vhj-b0bace6448ae4b0fbc1d5e323998a7d2' ",
                status=status.HTTP_400_BAD_REQUEST)

        hotel_data_json = self.get_hotel(property_id=property_id, request=request)
        hotel_data = load_and_dump_data(hotel_data_json)
        request_data = self.get_hotel_data_dict(hotel_data)
        serializer = HotelBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request_data)

        context_data = {
            'message': 'success',
            'data': request_data
        }
        return Response(context_data, status=status.HTTP_201_CREATED)


class HotelBookingsList(views.APIView):
    """
        Return the number of bookings per property the property ID from HERE places.
        * i.e here:pds:place:276u0vhj-b0bace6448ae4b0fbc1d5e323998a7d2

    """

    def get_queryset(self, id):
        return HotelBooking.objects.filter(property_id=id)

    @swagger_auto_schema(
        responses={200: HotelSerializer(many=True)})
    def get(self, request, **kwargs):
        queryset = self.get_queryset(id=kwargs['PROPERTY_ID'])
        serializer = HotelSerializer(queryset, many=True)

        context_data = {
            'message': 'success',
            'number_of_bookings': len(serializer.data),
            'data': serializer.data
        }
        return Response(context_data)
