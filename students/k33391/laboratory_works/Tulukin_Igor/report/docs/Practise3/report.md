# Практика 3.1

Модели

```
from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birthday = models.DateField()


class License(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Owner, related_name='licences', on_delete=models.CASCADE)
    license_type = models.CharField(max_length=100)
    date_given = models.DateField()


class Car(models.Model):
    num = models.CharField(max_length=100)
    mark = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=100)


class CarOwning(models.Model):
    start = models.DateField()
    finish = models.DateField()

    car = models.ForeignKey(Car, related_name='owners', on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, related_name='cars', on_delete=models.CASCADE)




```
Импорты
```
>>> from practice.models import *
>>> import datetime
>>> from django.db.models import Min, Max, Count


```

Создание объектов
```
>>> car1 = Car.objects.create(num='num1', mark='mark1', model='model1', color='black')
>>> car2 = Car.objects.create(num='num2', mark='mark1', model='model2', color='black')
>>> car3 = Car.objects.create(num='num3', mark='mark1', model='model3', color='black')
>>> car4 = Car.objects.create(num='num4', mark='mark2', model='model1', color='black')
>>> car5 = Car.objects.create(num='num5', mark='mark2', model='model2', color='black')
>>> car6 = Car.objects.create(num='num6', mark='mark2', model='model3', color='black')


>>> owner1 = Owner.objects.create(name='name1', surname='surname1', birthday=datetime.date.today())
>>> owner2 = Owner.objects.create(name='name2', surname='surname2', birthday=datetime.date.today())
>>> owner3 = Owner.objects.create(name='name3', surname='surname3', birthday=datetime.date.today())
>>> owner4 = Owner.objects.create(name='name4', surname='surname4', birthday=datetime.date.today())
>>> owner5 = Owner.objects.create(name='name5', surname='surname5', birthday=datetime.date.today())
>>> owner6 = Owner.objects.create(name='name6', surname='surname6', birthday=datetime.date.today())

>>>license1 = License.objects.create(name='licence1', owner=owner1, license_type='type1', date_given=datetime.date.today())
>>>license2 = License.objects.create(name='licence2', owner=owner2, license_type='type1', date_given=datetime.date.today())
>>>license3 = License.objects.create(name='licence3', owner=owner3, license_type='type1', date_given=datetime.date.today())
>>>license4 = License.objects.create(name='licence4', owner=owner4, license_type='type2', date_given=datetime.date.today())
>>>license5 = License.objects.create(name='licence5', owner=owner5, license_type='type2', date_given=datetime.date.today())

>>>car_owing1 = CarOwning.objects.create(start=datetime.date.today(), finish=datetime.date.today(),
                                      car=car1, owner=owner1)
>>>car_owing2 = CarOwning.objects.create(start=datetime.date.today(), finish=datetime.date.today(),
                                      car=car2, owner=owner2)
>>>car_owing3 = CarOwning.objects.create(start=datetime.date.today(), finish=datetime.date.today(),
                                      car=car3, owner=owner3)
>>>car_owing4 = CarOwning.objects.create(start=datetime.date.today(), finish=datetime.date.today(),
                                      car=car4, owner=owner4)
>>>car_owing5 = CarOwning.objects.create(start=datetime.date.today(), finish=datetime.date.today(),
                                      car=car5, owner=owner5)
>>>car_owing6 = CarOwning.objects.create(start=datetime.date.today(), finish=datetime.date.today(),
                                      car=car6, owner=owner6)

```


Выведете все машины марки “Toyota” (или любой другой марки, которая у вас есть)

```
>>> Car.objects.filter(mark='mark1')
<QuerySet [<Car: Car object (1)>, <Car: Car object (2)>, <Car: Car object (3)>, <Car: Car object (7)>, <Car: Car object (8)>, <Car: Car object (9)>]>
```

Найти всех водителей с именем “Олег” (или любым другим именем на ваше усмотрение)

```
>>> Owner.objects.filter(name='name1')
<QuerySet [<Owner: Owner object (1)>, <Owner: Owner object (7)>]>
```
Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели (можно в 2 запроса)

```
>>> License.objects.filter(owner_id=7)
<QuerySet [<License: License object (1)>]>
```

Вывести всех владельцев красных машин (или любого другого цвета, который у вас присутствует)

```
>>> Car.objects.filter(color='black')
<QuerySet [<Car: Car object (1)>, <Car: Car object (2)>, <Car: Car object (3)>, <Car: Car object (4)>, <Car: Car object (5)>, <Car: Car object (6)>]>
```

Найти всех владельцев, чей год владения машиной начинается с 2010 (или любой другой год, который присутствует у вас в базе)

```
>>> Owner.objects.filter(cars__start__gt=datetime.date(year=2010, month=1, day=1),
...                           cars__start__lt=datetime.date(year=2011, month=1, day=1))
<QuerySet []>
>>> Owner.objects.filter(cars__start__gt=datetime.date(year=2024, month=1, day=1), cars__start__lt=datetime.date(year=2025, month=1, day=1))
<QuerySet [<Owner: Owner object (7)>, <Owner: Owner object (8)>, <Owner: Owner object (9)>, <Owner: Owner object (10)>, <Owner: Owner object (11)>, <Owner: Owner object (12)>]>

```
Вывод даты выдачи самого старшего водительского удостоверения

```
>>> License.objects.aggregate(date_given=Min('date_given'))
{'date_given': datetime.date(2024, 1, 10)}

```

Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе

```
>>> CarOwning.objects.aggregate(date_given=Max('finish'))
{'date_given': datetime.date(2024, 1, 10)}

```
Выведите количество машин для каждого водителя

```
>>> counts = Owner.objects.annotate(Count("cars"))
>>> for count in counts:
...     print(count.name, count.cars__count)
... 
name1 1
name2 1
name3 1
name4 1
name5 1
name6 1

```

Подсчитайте количество машин каждой марки

```
>>> Car.objects.values("mark").annotate(Count("id"))
<QuerySet [{'mark': 'mark1', 'id__count': 6}, {'mark': 'mark2', 'id__count': 6}]>
```

Отсортируйте всех автовладельцев по дате выдачи удостоверения

```
>>> CarOwning.objects.order_by("owner__licences__date_given")
<QuerySet [<CarOwning: CarOwning object (1)>, <CarOwning: CarOwning object (2)>, <CarOwning: CarOwning object (3)>, <CarOwning: CarOwning object (4)>, <CarOwning: CarOwning object (5)>, <CarOwning: CarOwning object (6)>, <CarOwning: CarOwning object (12)>, <CarOwning: CarOwning object (7)>, <CarOwning: CarOwning object (8)>, <CarOwning: CarOwning object (9)>, <CarOwning: CarOwning object (10)>, <CarOwning: CarOwning object (11)>]>
```

