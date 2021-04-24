from rest_framework import serializers
from .models import Eventhall, Booking

class EventhallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Eventhall
        fields = ['name','capacity','location','tags']

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'