from rest_framework import serializers
from .models import HotelBooking
from drf_yasg import openapi




# class HotelBookingSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = HotelBooking
#         fields = ('created_at', 'hotel_name', 'hotel_id', 'postal_code',
#                   'latitude', 'longitude')


class HotelBookingSerializer(serializers.Serializer):
    hotel_id = serializers.CharField(help_text='The property id from HERE places')


    def create(self, validated_data):
        return HotelBooking.objects.create(**validated_data)


