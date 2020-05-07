
from django.urls import path
from .views import ListHotels, HotelBookingsCreate, HotelBookingsList


urlpatterns = [
    path('properties',
         ListHotels.as_view(), name='list_hotels'),
    path('properties/<PROPERTY_ID>/bookings',
         HotelBookingsList.as_view(), name='hotel_bookings_list'),
    path('bookings/', HotelBookingsCreate.as_view(), name='create_booking'),

]
