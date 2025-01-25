from django.contrib import admin

# Register your models here.
from . models import User, appointment, Prescription

admin.site.register(User)
admin.site.register(appointment)
admin.site.register(Prescription)