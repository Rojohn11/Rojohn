from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import EventhallSerializer, BookingSerializer, ReviewSerializer
from .models import Eventhall, Booking, Review
# Create your views here.

class EventhallListAPIView(ListCreateAPIView):
    serializer_class = EventhallSerializer
    queryset = Eventhall.objects.all()
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            




class EventhallDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = EventhallSerializer 
    queryset = Eventhall.objects.all()

    def get():


  

class BookingListAPIView(ListCreateAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def get(self, *args, **kwargs):

    


class BookingDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def get():



class ReviewListAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


    def get():

        