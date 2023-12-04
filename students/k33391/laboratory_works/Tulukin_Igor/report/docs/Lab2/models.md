# Models.py

**Задача**: Реализовать модели для реализации сайта по соответствующей предметной области "Табло отображения информации об авиаперелетах"

**Реализация**: Были реализованы следующие модели: 

- Пользователь
- Рейс
- Билет
- Место
- Комментарий

**Листинг кода**:
``` py title="Models.py"
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    passport = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.passport}"


class Seat(models.Model):
    flight = models.ForeignKey('main_app.Flight', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Flight(models.Model):
    flight_number = models.CharField(max_length=100)
    time = models.DateTimeField()
    destination = models.CharField(max_length=100)
    air_line = models.CharField(max_length=100)

    TYPES = models.TextChoices('type', ['arrive', 'departure'])
    type = models.CharField(max_length=20, choices=TYPES.choices)
    gate = models.CharField(max_length=10)


class Ticket(models.Model):
    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seat = models.OneToOneField('main_app.Seat',  on_delete=models.CASCADE)
    number = models.CharField(max_length=100)


class Comment(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    message = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
```
