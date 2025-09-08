from django.contrib import admin

from .models import CarMake, CarModel

# Register your models here.

admin.site.register(CarMake)
admin.site.register(CarModel)

# # CarModelInline class
# class CarModelInline(admin.TabularInline):
#     model = CarModel
#     extra = 1


# # CarModelAdmin class
# class CarModelAdmin(admin.ModelAdmin):
#     list_display = ("name", "car_make", "car_type", "year")
#     search_fields = ("name", "car_make__name")
#     list_filter = ("car_type", "year")


# admin.site.register(CarModel, CarModelAdmin)


# # CarMakeAdmin class with CarModelInline
# class CarMakeAdmin(admin.ModelAdmin):
#     inlines = [CarModelInline]


# admin.site.register(CarMake, CarMakeAdmin)
