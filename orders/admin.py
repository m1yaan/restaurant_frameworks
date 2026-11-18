from django.contrib import admin
from .models import Client, Table, Dish, Order, OrderItem
admin.site.register([Client, Table, Dish, Order, OrderItem])
