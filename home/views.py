from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from datetime import date, datetime

from .models import HourlyWeather, DailyWeather
from .utils import water_func, water_modify, call_web

# Create your views here.

# View for dashboard
def dashboard(request):
    # fetch current weather data
    latest_hourly = HourlyWeather.objects.first()
    latest_daily = DailyWeather.objects.first()

    # decide if watering is necessary (automated decision)
    watering_decision = water_func()  # result is a string

    # handle manual watering control
    if request.method == "POST":
        action = request.POST.get("action")  # "start" or "stop"
        if action == "start":
            message = "Manual watering started"
            return JsonResponse({"message":message})
        elif action == "stop":
            message = "Manual watering stopped"
            return JsonResponse({"message":message})
        else:
            return JsonResponse({"error":"Invalid action"})
    
    # pass weather data and decision to the template
    context = {
        "latest_hourly":latest_hourly,
        "latest_daily":latest_daily,
        "watering_decision":watering_decision,
    }
    return render(request, "dashboard.html", context)

