from django.db import models
from accounts.models import User

# Create your models here.

class Eventhall(models.Model):

    name = models.CharField(max_length=50)
    capacity = models.IntegerField()
    location = models.CharField(max_length=100)
    tags = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Booking(models.Model):
    BOOKING_STATUSES = (
        ('BOK', 'BOOKED'),
        ('CAN', 'CANCELED'),
    )

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    eventhall = models.ForeignKey(to=Eventhall, on_delete=models.CASCADE)
    bookeddate = models.DateTimeField(auto_now_add=True)
    booking_status = models.CharField(max_length=3, choices=BOOKING_STATUSES)

class Review(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    message = models.CharField(max_length=365)




