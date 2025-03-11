from django.core.management.base import BaseCommand
from django.utils import timezone
import requests
from datetime import datetime, date
from home.models import HourlyWeather, DailyWeather


class Command(BaseCommand):
    help = "Fetch weather data from API and save to the database"

    def handle(self, *args, **kwargs):
        # Fetch data logic
        URL = "https://api.open-meteo.com/v1/forecast?latitude=45.3382878&longitude=14.4338034&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,soil_moisture_1_to_3cm&daily=precipitation_sum&timezone=Europe%2FBerlin"
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()

            # Process and save hourly data
            hourly_data = data.get("hourly", {})  # this is a dict
            timestamps = hourly_data.get("time", [])
            temperatures = hourly_data.get("temperature_2m", [])
            relative_humidity = hourly_data.get("relative_humidity_2m", [])
            soil_moisture = hourly_data.get("soil_moisture_1_to_3cm", []) 
            precipitation_probs = hourly_data.get("precipitation_probability", [])

            for i in range(len(timestamps)):
                HourlyWeather.objects.create(
                    timestamp=timezone.make_aware(datetime.fromisoformat(timestamps[i])),
                    temperature_2m=temperatures[i],
                    relative_humidity_2m = relative_humidity[i],
                    soil_moisture_1_to_3cm = soil_moisture[i],
                    precipitation_probability = precipitation_probs[i],
                )

            # Process and save daily data
            daily_data = data.get("daily", {})
            dates = daily_data.get("time", [])
            precipitation_sums = daily_data.get("precipitation_sum", [])


            for i in range(len(dates)):
                DailyWeather.objects.create(
                    date=date.fromisoformat(dates[i]),
                    precipitation_sum=precipitation_sums[i],
                )

        self.stdout.write(self.style.SUCCESS("Weather data fetched and saved."))
