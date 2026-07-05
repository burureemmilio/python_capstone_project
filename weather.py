import requests

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


def get_available_times(forecast_data, selected_date):
    times = []

    for item in forecast_data["list"]:
        date, time = item["dt_txt"].split()

        if date == selected_date:
            times.append(time)

    return times


def get_selected_forecast(forecast_data, selected_date, selected_time):
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