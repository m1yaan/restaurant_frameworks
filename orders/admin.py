from django.contrib import admin
from .models import Client, Table, Dish, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email")
    search_fields = ("name", "phone", "email")
    ordering = ("name",)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "capacity", "is_active")
    list_filter = ("is_active",)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name", "category")
    list_editable = ("price", "is_available")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "table", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("client__name", "client__phone")
    inlines = [OrderItemInline]
    date_hierarchy = "created_at"
