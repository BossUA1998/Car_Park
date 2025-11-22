from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from Car_service.models import Car, Manufacturer, Seller


admin.site.unregister(Group)


@admin.register(get_user_model())
class ClientAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("is_seller",)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = admin.ModelAdmin.list_display + ("owner", "year", "mileage", "manufacturer")
    list_filter = ("year", "mileage")
    search_fields = ("model",)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = admin.ModelAdmin.list_display + ("country",)
    list_filter = ("country",)
    search_fields = ("name",)
