from django.shortcuts import render
from rest_framework import views, status, generics
from rest_framework.response import Response
import requests
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ValidationError
from .serializers import HotelBookingSerializer
from .utlis import load_and_dump_data
from .models import HotelBooking


class ListHotels(views.APIView):
    """
    View to list all hotels in a given area.

    * Requires the cordinates of the area i.e Longitude and Langtitude.
    * 
    """

    def get(self, request, format=None):
        """
        Return a list of all hotels in a given area.

        * Requires LAT,LONG of the area in the url
        * i.e https://curanetwork.herokuapp.com/api/properties?at=LAT,LONG

        """
        try:
            cordinates = request.GET['at']

            if(len(cordinates.split(',')) != 2):
                raise ValidationError(
                    'You need to input both the Latitude and Longitude')

            BASE_URL = 'https://discover.search.hereapi.com/v1/discover?q=hotels'
            request_url = f'{BASE_URL}&at={cordinates}&apiKey={settings.HERE_API_KEY}'

            try:
                is_cached = request.session['cordinates'] == cordinates
            except KeyError:
                is_cached = False
                request.session['cordinates'] = cordinates

            if not is_cached:
                response = requests.get(request_url).json()
                request.session['hotels_data'] = response
                request.session['cordinates'] = cordinates

            hotels_data = request.session['hotels_data']

        except MultiValueDictKeyError:
            return Response("You need to include the at in the params i.e '&at=42.36399,-71.05493' ", status=status.HTTP_400_BAD_REQUEST)

        context = dict(message='success', data=hotels_data)
        return Response(context)


class HotelBookingsCreate(generics.CreateAPIView):
    serializer_class = HotelBookingSerializer

    def get_hotel(self, request, hotel_id):
        BASE_URL = 'https://lookup.search.hereapi.com/v1/lookup?id='
        request_url = f'{BASE_URL}{hotel_id}&apiKey={settings.HERE_API_KEY}'

        try:
            is_cached = request.session['hotel_id'] == hotel_id
        except KeyError:
            is_cached = False
            request.session['hotel_id'] = hotel_id

        if not is_cached:
            response = requests.get(request_url).json()
            request.session['hotel_data'] = response
            request.session['hotel_id'] = hotel_id

        hotel_data = request.session['hotel_data']

        return hotel_data

    def get_hotel_data_dict(self, hotel_data):
        hotel_title = hotel_data['title']
        hotel_id = hotel_data['id']
        postal_code = hotel_data['address']['postalCode']
        latitude = hotel_data['position']['lat']
        longitude = hotel_data['position']['lng']
        phone_number = hotel_data['contacts'][0]['phone'][0]['value']
        email = hotel_data['contacts'][0]['email'][0]['value']

        request_data = dict(hotel_name=hotel_title, hotel_id=hotel_id, postal_code=postal_code,
                            latitude=latitude, longitude=longitude, phone_number=phone_number, email=email)

        return request_data

    def create(self, request, *args, **kwargs):
        try:
            hotel_id = request.data['hotel_id']
        except MultiValueDictKeyError:
            return Response("You need to include the hotel_id in the request body i.e 'here:pds:place:276u0vhj-b0bace6448ae4b0fbc1d5e323998a7d2' ", status=status.HTTP_400_BAD_REQUEST)

        hotel_data_json = self.get_hotel(hotel_id=hotel_id, request=request)
        hotel_data = load_and_dump_data(hotel_data_json)
        request_data = self.get_hotel_data_dict(hotel_data)
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        context_data = {
            'message': 'success',
            'data': serializer.data
        }
        return Response(context_data, status=status.HTTP_201_CREATED, headers=headers)


class HotelBookingsList(generics.ListAPIView):
    serializer_class = HotelBookingSerializer

    def get_queryset(self, id):
        # id = self.request.get['PROPERTY_ID']
        return HotelBooking.objects.filter(hotel_id=id)

    def list(self, request, PROPERTY_ID):
        queryset = self.get_queryset(id=PROPERTY_ID)
        serializer = HotelBookingSerializer(queryset, many=True)

        context_data = {
            'message': 'success',
            'number_of_bookings': len(serializer.data),
            'data': serializer.data
        }
        return Response(context_data)
