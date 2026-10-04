"""Django admin configuration for vehicle inventory."""

from django.contrib import admin

from .models import CarMake, CarModel


class CarModelInline(admin.TabularInline):
    """Edit car models within their manufacturer."""

    model = CarModel
    extra = 1


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    """Admin view for car manufacturers."""

    list_display = ("name", "description")
    search_fields = ("name",)
    inlines = (CarModelInline,)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    """Admin view for car models."""

    list_display = ("name", "car_make", "car_type", "year")
    list_filter = ("car_make", "car_type", "year")
