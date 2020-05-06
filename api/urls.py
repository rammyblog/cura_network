
from django.urls import path
from .views import ListHotels, HotelBookingsCreate, HotelBookingsList


urlpatterns = [
    path('properties',
         ListHotels.as_view(), name='List_Hotels'),
    path('properties/<PROPERTY_ID>/bookings',
         HotelBookingsList.as_view(), name='Hotel_bookings_list'),
    path('bookings/', HotelBookingsCreate.as_view(), name='Create_booking'),

]
