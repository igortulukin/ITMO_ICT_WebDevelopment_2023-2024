# Views.py
**Листинг кода**:
``` py title="views.py"
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, SAFE_METHODS
from . import serializers
from .models import *
import datetime


class VisiterViewSet(ModelViewSet):
    queryset = Visiter.objects.all()
    serializer_class = serializers.VisiterSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]


class LivingViewSet(ModelViewSet):
    queryset = Living.objects.all()
    serializer_class = serializers.LivingSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]


    def get_serializer_class(self):
        if self.action == "get_visiters_from":
            return serializers.CitySerializer
        if self.action == "who_cleans":
            return serializers.DayOfTheWeekSerializer
        else:
            return serializers.VisiterSerializer

    @action(detail=False, methods=["Post"])
    def get_visiters_from(self, request):
        obj = self.get_object()
        city = request.data.get("name", None)
        if city:
            vis = Visiter.objects.filter(fr__name=city)
            ser = serializers.VisiterSerializer(vis, many=True)
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["Post"])
    def who_cleans(self, request, pk=None):
        obj = self.get_object()
        day = request.data.get("day", None)
        if day:
            room = Room.objects.filter(living_who__in=Living.objects.filter(visiter=obj.id))
            cleaning = Cleaning.objects.filter(room=room.id, day_of_week=day)
            ser = serializers.CleaningSerializer(cleaning)
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == "get_living_by_date":
            return serializers.DateSerializer
        else:
            return serializers.RoomSerializer

    @action(detail=True, methods=["Post"])
    def get_living_by_date(self, request, pk=None):
        obj = self.get_object()
        date = request.data.get("date", None)

        if date:
            livings = Living.objects.filter(room=obj.id, date_start__lt=date, date_end__gt=date)
            ser = serializers.LivingSerializer(livings, many=True)
            return Response(ser.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"])
    def get_living_by_date(self, request):
        qs = Room.objects.none()

        for obj in Room.objects.all():
            if not Living.objects.filter(room=obj.id, date_start__lt=datetime.date.today(), date_end__gt=datetime.date.today()):
                qs |= Room.objects.filter(id=obj.id)

        ser = serializers.RoomSerializer(qs, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class FloorViewSet(ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = serializers.FloorSerializer
    permission_classes = [IsAuthenticated]


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = serializers.CitySerializer
    permission_classes = [IsAuthenticated]


class WorkerViewSet(ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = serializers.WorkerSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]


class CleaningViewSet(ModelViewSet):
    queryset = Cleaning.objects.all()
    serializer_class = serializers.CleaningSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

```