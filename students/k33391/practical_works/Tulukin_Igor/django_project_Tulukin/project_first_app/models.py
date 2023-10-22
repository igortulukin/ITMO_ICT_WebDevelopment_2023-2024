from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(default='None', max_length=30)
    first_name = models.CharField(default='None',max_length=30)
    passport_number = models.CharField(default='------', max_length=8)
    home_address = models.CharField(default='------', max_length=50)
    nationality = models.CharField(default='------', max_length=20)
    birthday = models.DateTimeField(default=datetime.now(), blank=True)



class Car(models.Model):
    id = models.AutoField(primary_key=True)
    state_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, blank=True)


class Ownership(models.Model):
    id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True)


class DriversLicense(models.Model):
    id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    issue_date = models.DateTimeField(max_length=30)
