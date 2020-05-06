from rest_framework import serializers
from .models import HotelBooking


class HotelBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelBooking
        fields = ('created_at', 'hotel_name', 'hotel_id', 'postal_code',
                  'latitude', 'longitude')
