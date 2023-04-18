from django.contrib import admin
from .models import Menu, Category, Order, Booking
# Register your models here.

admin.site.register(Menu)
admin.site.register(Booking)
admin.site.register(Category)
admin.site.register(Order)
