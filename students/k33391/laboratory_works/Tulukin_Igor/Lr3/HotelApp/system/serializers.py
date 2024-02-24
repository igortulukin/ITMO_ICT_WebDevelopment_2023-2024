from rest_framework import serializers
from .models import *


class VisiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visiter
        fields ="__all__"


class LivingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Living
        fields ="__all__"


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields ="__all__"


class DateSerializer(serializers.Serializer):

    date = serializers.DateField()
    class Meta:
        fields = ['date']


class DayOfTheWeekSerializer(serializers.Serializer):
    day = serializers.CharField()
    class Meta:
        fields = ['day']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields ="__all__"


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields ="__all__"


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = "__all__"


class CleaningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cleaning
        fields = "__all__"

class ShowCleaningSerializer(serializers.ModelSerializer):
    clearer = WorkerSerializer()
    floor = FloorSerializer()
    class Meta:
        model = Cleaning
        fields = ['id', 'day_of_week', 'clearer', 'floor']