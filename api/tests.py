import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import HotelBooking


class PropertyTests(APITestCase):
    def test_create_booking(self):
        """
        Ensure we can create a new booking object and get the booking count for that booking.
        """
        url = reverse('create_booking')
        data = {
            'property_id': 'here:pds:place:250spd1v-f4f21f5191334952af0b22e52f4d7828'}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HotelBooking.objects.count(), 1)
        self.assertEqual(HotelBooking.objects.get().property_id,
                         'here:pds:place:250spd1v-f4f21f5191334952af0b22e52f4d7828')

    def test_count_booking(self):
        """
            Ensure we can create a new booking object and get the booking counts for a particular hotel ID.
        """

        create_booking_url = reverse('create_booking')
        booking_count_url = reverse('hotel_bookings_list',
                                    kwargs={'PROPERTY_ID': 'here:pds:place:250spd1v-f4f21f5191334952af0b22e52f4d7828'})
        data = {
            'property_id': 'here:pds:place:250spd1v-f4f21f5191334952af0b22e52f4d7828'}
        create_response = self.client.post(
            create_booking_url, data=data, format='json')
        count_response = self.client.get(booking_count_url, format='json')

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(count_response.status_code, status.HTTP_200_OK)
        self.assertEqual(count_response.data['number_of_bookings'], 1)

    def test_get_properties(self):
        """
            Ensure we can get a list of properties using their cordinates (Latitude and Longitude).
        """
        response = self.client.get(
            '/api/properties?at=42.36399,-71.1', format='json')
        test_dict = json.loads(response.content)
        response_test_data = test_dict['data']['items'][0]
        test_data = {'title': 'Boston Marriott Cambridge',
                     'id': 'here:pds:place:840drt2y-3108ffe3c27b42d1ac86c8938c523f68',
                     'resultType': 'place',
                     'address': {'label': 'Boston Marriott Cambridge, 50 Broadway, Cambridge, MA 02142, United States',
                                 'countryCode': 'USA', 'countryName': 'United States', 'state': 'Massachusetts',
                                 'county': 'Middlesex', 'city': 'Cambridge', 'district': 'MIT', 'street': 'Broadway',
                                 'postalCode': '02142', 'houseNumber': '50'},
                     'position': {'lat': 42.36294, 'lng': -71.0858},
                     'access': [{'lat': 42.36314, 'lng': -71.08564}], 'distance': 1173,
                     'categories': [{'id': '200-2200-0000'}, {'id': '500-5000-0000'}, {'id': '500-5000-0053'}],
                     'contacts': [
                         {'phone': [{'value': '+16174946600'}], 'tollFree': [{'value': '+18002289290'}],
                          'fax': [{'value': '+16174940036'}], 'www': [{'value': 'http://www.marriott.com/'}, {
                              'value': 'http://www.marriott.com/hotels/travel/boscb-boston-marriott-cambridge/'}]}],
                     'openingHours': [{'text': ['Mon-Sun: 00:00 - 24:00'], 'isOpen': True, 'structured': [
                         {'start': 'T000000', 'duration': 'PT24H00M',
                          'recurrence': 'FREQ:DAILY;BYDAY:MO,TU,WE,TH,FR,SA,SU'}]}]}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_test_data, test_data)
