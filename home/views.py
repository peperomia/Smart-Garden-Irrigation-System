from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from datetime import date, datetime
import json

from .models import HourlyWeather, DailyWeather
from .utils import water_func, water_modify, call_web

# Create your views here.

# View for dashboard
def dashboard(request):
    """Zvone napisao ovu funkciju"""
    # Fetch current weather data
    now = datetime.now()
    today = date.today()
    timestamp_to_seek = datetime(now.year, now.month, now.day, now.hour, 0)
    print("today", today)
    print("timestamp_to_seek: ", timestamp_to_seek)
    latest_hourly = HourlyWeather.objects.filter(timestamp=timestamp_to_seek).first()
    latest_daily = DailyWeather.objects.filter(date=today).first()
    print("latest_hourly", latest_hourly)
    print("latest_daily", latest_daily)

    # Decide if watering is necessary (automated decision)
    watering_decision = water_func()  # Result is a string

    # Handle manual watering control
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            action = data.get("action")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        if action == "start":
            return JsonResponse({"message": "Manual watering started"})
        elif action == "stop":
            return JsonResponse({"message": "Manual watering stopped"})
        else:
            return JsonResponse({"error": "Invalid action"}, status=400)

    # Pass weather data and decision to the template
    context = {
        "latest_hourly": latest_hourly,
        "latest_daily": latest_daily,
        "watering_decision": watering_decision,
    }
    return render(request, "dashboard.html", context)

#------------------------------------------------------------
# funkcija koja radi, originalno ovdje 
# def dashboard(request):
#     # fetch current weather data
#     latest_hourly = HourlyWeather.objects.first()
#     latest_daily = DailyWeather.objects.first()

#     # decide if watering is necessary (automated decision)
#     watering_decision = water_func()  # result is a string

#     # handle manual watering control
#     if request.method == "POST":
#         action = request.POST.get("action")  # "start" or "stop"
#         if action == "start":
#             message = "Manual watering started"
#             return JsonResponse({"message":message})
#         elif action == "stop":
#             message = "Manual watering stopped"
#             return JsonResponse({"message":message})
#         else:
#             return JsonResponse({"error":"Invalid action"})
    
#     # pass weather data and decision to the template
#     context = {
#         "latest_hourly":latest_hourly,
#         "latest_daily":latest_daily,
#         "watering_decision":watering_decision,
#     }
#     return render(request, "dashboard.html", context)

