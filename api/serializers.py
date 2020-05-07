from rest_framework import serializers
from .models import HotelBooking
from drf_yasg import openapi




class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelBooking
        fields = '__all__'


class HotelBookingSerializer(serializers.Serializer):
    property_id = serializers.CharField(help_text='The property id from HERE places')


    def save(self, validated_data):
        return HotelBooking.objects.create(**validated_data)


