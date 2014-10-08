from django.db import models

# Create your models here.

class Trip(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)


class Segment(models.Model):
    id = models.IntegerField(primary_key=True)
    trip = models.ForeignKey(Trip)

    start_airport = models.CharField(max_length=4)
    start_city = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    start_ltlng = models.CharField(max_length=100) # lat,lng

    end_time = models.DateTimeField()
    end_airport = models.CharField(max_length=4)
    end_city = models.CharField(max_length=100)
    airline = models.CharField(max_length=40)
    end_ltlng = models.CharField(max_length=100) # lat,lng

    flight_number = models.IntegerField()
    distance_miles = models.IntegerField()
    duration_mins = models.IntegerField()
