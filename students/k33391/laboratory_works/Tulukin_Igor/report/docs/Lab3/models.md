# Models.py

**Задача**: Реализовать модели по соответствующей предметной области "Администратор гостиницы."

**Листинг кода**:
``` py title="Models.py"
from django.db import models


class Floor(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Room(models.Model):
    num = models.CharField(max_length=10)
    type = models.CharField(max_length=10, choices=(("1", "1"), ("2", "2"), ("3", "3")))
    cost = models.FloatField()
    telephone = models.CharField(max_length=15)


class City(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Visiter(models.Model):
    name = models.CharField(max_length=500)
    passport = models.CharField(max_length=30)
    fr = models.ForeignKey("system.City", related_name="visiters_from", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Living(models.Model):
    visiter = models.ForeignKey("system.Visiter", related_name="living_where", on_delete=models.CASCADE)
    room = models.ForeignKey("system.Room", related_name="living_who", on_delete=models.CASCADE)

    date_start = models.DateField()
    date_end = models.DateField()


class Worker(models.Model):
    name = models.CharField(max_length=500)


class Cleaning(models.Model):
    clearer = models.ForeignKey("system.Worker", related_name="clearing_where", on_delete=models.CASCADE)
    floor = models.ForeignKey("system.Floor", related_name="clearing_who", on_delete=models.CASCADE)

    day_of_week = models.CharField(max_length=10, choices=(("mn", "mn"),    ("tu", "tu"),
                                                           ("we", "we"),    ("th", "th"),
                                                           ("fr", "fr"),    ("sa", "sa"),
                                                           ("su", "su")))

```
