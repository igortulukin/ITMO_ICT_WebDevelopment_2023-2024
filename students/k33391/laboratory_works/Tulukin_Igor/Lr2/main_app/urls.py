from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", views.register, name="user_register"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),


    path("flights/", views.flights_list, name="flights_list"),
    path("flights/<int:flight_id>/", views.flight_detail, name="flight_detail"),
    path("ticket/<int:flight_id>/", views.buy_ticket, name="buy_ticket"),

    path("tickets/", views.tickets_for_user, name="tickets_for_user"),
    path("tickets/<int:ticket_id>/", views.ticket_update, name="ticket_update"),
    path("tickets/<int:ticket_id>/delete", views.ticket_delete, name="ticket_delete"),
]