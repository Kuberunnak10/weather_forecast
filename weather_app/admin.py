from django.contrib import admin

from weather_app.models import WeatherModel


# Register your models here.
@admin.register(WeatherModel)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ('city', 'user')
    list_filter = ('user',)
