from django.contrib import admin
from .models import Owner, Ownership, Car, DriversLicense

admin.site.register(Ownership)
admin.site.register(Car)
admin.site.register(DriversLicense)
admin.site.register(Owner)
