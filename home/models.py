from django.db import models

# Create your models here.

# upisati direktno na stranici
# latitude = models.FloatField()
# longitude = models.FloatField()

class HourlyWeather(models.Model):
    timestamp = models.DateTimeField()
    temperature_2m = models.FloatField()
    relative_humidity_2m = models.FloatField()
    soil_moisture_1_to_3cm = models.FloatField()
    precipitation_probability = models.FloatField()

    def __str__(self):
        return f"Hourly data at {self.timestamp}: {self.temperature_2m}°C"


class DailyWeather(models.Model):
    date = models.DateField()
    precipitation_sum = models.FloatField()

    def __str__(self):
        return f"Daily data on {self.date}: {self.precipitation_sum}mm"
    





