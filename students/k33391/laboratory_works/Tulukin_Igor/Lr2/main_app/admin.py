from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Flight)
admin.site.register(models.Seat)
admin.site.register(models.Ticket)
admin.site.register(models.Comment)