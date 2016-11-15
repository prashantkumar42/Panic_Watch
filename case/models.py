import datetime

from django.contrib.auth.models import Permission, User
from django.db import models


class Case(models.Model):  # to store information for a case, primary key being the case id
    user = models.ForeignKey(User, default=1)  # user will be a Foreign key for a case
    watch_id = models.CharField(max_length=250)
    victim_name = models.CharField(max_length=500)
    date_created = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.watch_id + ' - ' + self.victim_name


class Coordinate(models.Model):  # to store coordinates corresponding to a case
    case = models.ForeignKey(Case, on_delete=models.CASCADE)  # case will be a Foreign key for Coordinates
    latitude = models.CharField(max_length=250)
    longitude = models.CharField(max_length=250)
    date_created = models.DateTimeField(default=datetime.datetime.now)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.latitude + ' - ' + self.longitude
