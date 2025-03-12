import requests
import json
from datetime import date, datetime

URL = "https://api.open-meteo.com/v1/forecast?latitude=45.3382878&longitude=14.4338034&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,soil_moisture_1_to_3cm&daily=precipitation_sum&timezone=Europe%2FBerlin"

def call_web(url = URL):
    try:
        response = requests.get(url)  # a json
        response.raise_for_status()
        data = response.json()
        # turn "time" data from iso8601 to datetime format
        hourly_time_iso = data["hourly"]["time"]
        hourly_time = list(map(lambda x: datetime.fromisoformat(x), hourly_time_iso))
        daily_time_iso = data["daily"]["time"]
        daily_time = list(map(lambda x: date.fromisoformat(x), daily_time_iso))

        data["hourly"]["time"] = hourly_time
        data["daily"]["time"] = daily_time

        return data
    except requests.HTTPError:
        # Handle error:
        try:
            with open("forecast.json", "r") as file:
                data = json.load(file)
                # turn timestamp data form iso8601 to datetime using .fromisoformat()
                hourly_time_iso = data["hourly"]["time"]
                hourly_time = list(map(lambda x: datetime.fromisoformat(x), hourly_time_iso))
                daily_time_iso = data["daily"]["time"]
                daily_time = list(map(lambda x: date.fromisoformat(x), daily_time_iso))

                data["hourly"]["time"] = hourly_time
                data["daily"]["time"] = daily_time

            return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
        

def water_func():
    """Function to decide watering."""
    data = call_web()
    if not data:
        return "Error: Could not fetch weather data."
    
    DAILY_DATA = data.get("daily", {})
    HOURLY_DATA = data.get("hourly", {})
    now = datetime.now()
    today = now.date()
    
    # for now: when you runserver the application, it will check in that moment whether to water or not

    # get today's index
    try:
        index_today = DAILY_DATA["time"].index(today)
        index_now = HOURLY_DATA["time"].index(datetime(now.year, now.month, now.day, now.hour, 0))
    except (ValueError, KeyError):
        return "Error: Missing data."
    
    # Check condititons
    precipitation = DAILY_DATA["precipitation_sum"][index_today]
    soil_moisture = HOURLY_DATA["soil_moisture_1_to_3cm"][index_now]
    if soil_moisture < 0.2 and precipitation < 1:
        return "Water Regular" if water_modify(now=now, today=today) == 0 else "Water Extra"
    else:
        return "Not Watering"
    

def water_modify(now, today):
    """Function to calculate extra watering"""
    data = call_web()

    if not data:
        return 0  # Assume no extra watering if data inavailable
    
    HOURLY_DATA = data.get("hourly", {})
    try:
        index_now = HOURLY_DATA["time"].index(datetime(now.year, now.month, now.day, now.hour, 0))
        index_plus12 = index_now + 12  # case when +12 is the tomorrow day accounted
    except (ValueError, KeyError):
        return 0
    
    # calculate averages:
    precipitation_outlook = sum(HOURLY_DATA["precipitation_probability"][index_now:index_plus12]/12)
    humidity = sum(HOURLY_DATA["relative_humidity_2m"][index_now:index_plus12]/12)
    temperature = sum(HOURLY_DATA["temperature_2m"][index_now:index_plus12]/12)

    return 10 if (precipitation_outlook<50) and (humidity<60) and (temperature>20) else 0





    


