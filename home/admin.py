from django.contrib import admin
from .models import HourlyWeather, DailyWeather

# Register your models here.
# admin.site.register(HourlyWeather)
# admin.site.register(DailyWeather)

from django.contrib import admin
from .models import HourlyWeather, DailyWeather

# Custom admin for HourlyWeather model
@admin.register(HourlyWeather)
class HourlyWeatherAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('timestamp', 'temperature_2m', 'relative_humidity_2m', 'precipitation_probability', 'soil_moisture_1_to_3cm')
    
    # Fields you can search in the admin interface
    search_fields = ('timestamp',)
    
    # Fields for filtering data
    list_filter = ('timestamp', 'temperature_2m')

# Custom admin for DailyWeather model
@admin.register(DailyWeather)
class DailyWeatherAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('date', 'precipitation_sum')
    
    # Fields you can search in the admin interface
    search_fields = ('date',)
    
    # Fields for filtering data
    list_filter = ('date',)


