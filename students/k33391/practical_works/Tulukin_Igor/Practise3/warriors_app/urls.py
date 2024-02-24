from django.urls import path
from .views import *

app_name = "warriors_app"

urlpatterns = [
    path("warriors/", WarriorAPIView.as_view()),
    path("profession/create/", ProfessionCreateView.as_view()),
    path("professions/", ProfessionAPIView.as_view()),
    path("skills/", SkillAPIView.as_view()),
    path("skill/create/", SkillCreateView.as_view()),
    path("warriors/<int:pk>/", WarriorDetail.as_view()),
]