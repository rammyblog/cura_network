from django.db import models
from django.utils import timezone


class HotelBooking(models.Model):
    property_name = models.CharField(max_length=1000)
    property_id = models.CharField(max_length=250)
    postal_code = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=False, default=timezone.now)

    def __str__(self):
        return f'{self.property_name} with ID: {self.property_id}'

    class Meta:

        verbose_name = 'HotelBooking'
        verbose_name_plural = 'HotelBookings'
