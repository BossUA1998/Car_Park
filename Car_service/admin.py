from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from Car_service.models import Car, Manufacturer, Seller


admin.site.unregister(Group)


@admin.register(get_user_model())
class ClientAdmin(UserAdmin):
    pass


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    pass


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    pass
