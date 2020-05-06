from django.db import models
from django.utils import timezone


class HotelBooking(models.Model):
    hotel_name = models.CharField(max_length=1000)
    hotel_id = models.CharField(max_length=250)
    postal_code = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=False, default=timezone.now)

    def __str__(self):
        return f'{self.hotel_name} with ID: {self.hotel_id}'

    class Meta:

        verbose_name = 'HotelBooking'
        verbose_name_plural = 'HotelBookings'


# {
#     "title": "Flughafen Frankfurt-Hahn",
#     "id": "here:pds:place:276u0vhj-b0bace6448ae4b0fbc1d5e323998a7d2",
#     "resultType": "place",
#     "address": {
#         "label": "Flughafen Frankfurt-Hahn, 55483 Lautzenhausen, Deutschland",
#         "countryCode": "DEU",
#         "countryName": "Deutschland",
#         "state": "Rheinland-Pfalz",
#         "county": "Rhein-Hunsrück-Kreis",
#         "city": "Lautzenhausen",
#         "postalCode": "55483"
#     },
#     "position": {
#         "lat": 49.94802,
#         "lng": 7.27153
#     },
#     "access": [
#         {
#             "lat": 49.94571,
#             "lng": 7.26985
#         }
#     ],
#     "categories": [
#         {
#             "id": "400-4000-4581"
#         }
#     ],
#     "contacts": [
#         {
#             "phone": [
#                 {
#                     "value": "+496543509200"
#                 }
#             ],
#             "www": [
#                 {
#                     "value": "http://www.hahn-airport.de"
#                 }
#             ],
#             "email": [
#                 {
#                     "value": "info@hahn-airport.de"
#                 }
#             ]
#         }
#     ]
# }
