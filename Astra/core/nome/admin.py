from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Staff, Attendance

admin.site.register(Staff)
admin.site.register(Attendance)
