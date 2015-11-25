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
    distance_miles = models.IntegerField(null=True)
    duration_mins = models.IntegerField()

    def __str__(self):
        return "<Segement {} {}>".format(self.airline, self.flight_number)

class TrainSegment(models.Model):
    id = models.IntegerField(primary_key=True)
    trip = models.ForeignKey(Trip)

    start_station = models.CharField(max_length=100)
    start_city = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    start_ltlng = models.CharField(max_length=100) # lat,lng

    end_station = models.CharField(max_length=100)
    end_city = models.CharField(max_length=100)
    end_time = models.DateTimeField()
    end_ltlng = models.CharField(max_length=100) # lat,lng

    train_number = models.IntegerField()
    duration_mins = models.IntegerField()
    carrier = models.CharField(max_length=40)

    def __str__(self):
        return "<TrainSegment {} {}>".format(self.carrier, self.train_number)

class TimeStamp(models.Model):
    timestamp = models.IntegerField()

    @classmethod
    def set(cls, val):
        ts =  cls.objects.get()
        ts.timestamp = val
        ts.save()

    @classmethod
    def get(cls):
        return cls.objects.get().timestamp

