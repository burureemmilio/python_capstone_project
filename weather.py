import requests
from datetime import datetime
api_key = "dd3d923481948739086ab7bd19423514"


def get_current_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(url)
    data = response.json()

    if data["cod"] != 200:
        return None, data["message"]

    weather_data = {
        "city": data["name"],
        "temperature": round(float(data["main"]["temp"]) - 273.15, 1),
        "condition": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }

    return weather_data, None


def get_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"

    response = requests.get(url)
    data = response.json()

    if data["cod"] != "200":
        return None, data["message"]

    return data, None


def get_available_dates(forecast_data):
    dates = []

    for item in forecast_data["list"]:
        date = item["dt_txt"].split()[0]

        if date not in dates:
            dates.append(date)

    return dates

def format_time_12hr(time_text):
    return datetime.strptime(time_text, "%H:%M:%S").strftime("%I:%M %p")

def get_available_times(forecast_data, selected_date):
    times = []

    for item in forecast_data["list"]:
        date, time = item["dt_txt"].split()

        if date == selected_date:
            times.append(format_time_12hr(time))

    return times

def get_available_time_slots(forecast_data, selected_date):
    raw_times = []

    for item in forecast_data["list"]:
        date, time = item["dt_txt"].split()

        if date == selected_date:
            raw_times.append(time)

    time_slots = []

    for i in range(len(raw_times)):
        start_time = raw_times[i]
        start_hour = int(start_time.split(":")[0])

        end_hour = start_hour + 3

        if end_hour >= 24:
            end_hour = end_hour - 24

        end_time = f"{end_hour:02d}:00:00"

        start_time_12hr = format_time_12hr(start_time)
        end_time_12hr = format_time_12hr(end_time)

        time_slots.append(f"{start_time_12hr} - {end_time_12hr}")

    return time_slots


def get_selected_forecast(forecast_data, selected_date, selected_time):
    # If selected_time is a range like "09:00:00 - 12:00:00",
    # use only the start time: "09:00:00"
    if " - " in selected_time:
        selected_time = selected_time.split(" - ")[0]
        
    selected_time = datetime.strptime(selected_time, "%I:%M %p").strftime("%H:%M:%S")

    for item in forecast_data["list"]:
        date, time = item["dt_txt"].split()

        if date == selected_date and time == selected_time:
            temperature = round(float(item["main"]["temp"]) - 273.15, 1)
            condition = item["weather"][0]["description"]
            humidity = item["main"]["humidity"]
            wind_speed = item["wind"]["speed"]

            return {
                "temperature": temperature,
                "condition": condition,
                "humidity": humidity,
                "wind_speed": wind_speed
            }

    return None

def get_weather_advice(condition):
    condition = condition.lower()

    if "rain" in condition:
        return "Carry an umbrella or consider rescheduling outdoor activities."
    elif "clear" in condition:
        return "Great weather for outdoor activities."
    elif "cloud" in condition:
        return "Weather looks okay, but it may feel cloudy."
    elif "storm" in condition or "thunder" in condition:
        return "Avoid outdoor activities if possible."
    else:
        return "Check conditions carefully before planning your task."