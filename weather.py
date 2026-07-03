#api key dd3d923481948739086ab7bd19423514
#endpoint - current forecast - https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
#endpoint - 5 day forecast - https://api.openweathermap.org/data/2.5/forecast?q={city name}&appid={API key}
import requests
import sqlite3
from datetime import datetime

conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS search_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    search_time TEXT
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT,
    city TEXT,
    task_date TEXT,
    task_time TEXT,
    weather_condition TEXT,
    temperature REAL,
    created_at TEXT
)
""")

conn.commit()

print("=" * 40)
print("         WEATHER DASHBOARD")
print("=" * 40)
def get_current_weather(city):
    api_key = "dd3d923481948739086ab7bd19423514"
    
    url_endpoint_current = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response1 = requests.get(url_endpoint_current)
    # print(response1)

    data_current = response1.json()
    #print(data_current)

    if data_current["cod"] != 200:
        print(f"Error: {data_current['message']}")

    #save_search(city)

    city_name = data_current['name']
    temp = round(int(data_current["main"]["temp"])-273.15, 1)
    weather =  data_current["weather"][0]["description"]
    humidity = data_current["main"]["humidity"]
    wind_speed = data_current["wind"]["speed"]
    
    
    print(f"\nWeather in {city_name}")
    print("-" * 30)
    print(f"Temperature: {temp}°C")
    print(f"Condition: {weather}")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed}m/s")

def save_search(city):
    search_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO search_history(city, search_time)
    VALUES (?, ?)
    """, (city, search_time))

    conn.commit()


#city = input("Enter your city: ")
#get_current_weather(city)

def get_forecast(city):
    api_key = "dd3d923481948739086ab7bd19423514"
    url_endpoint_forecast = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"

    response2 = requests.get(url_endpoint_forecast)
    #print(response2)

    data_forecast = response2.json()
    #print(data_forecast)
    if data_forecast["cod"] != "200":
        print(f"Error: {data_forecast['message']}")
        return None

    return data_forecast

def get_available_dates(forecast_data):
    dates = []

    for item in forecast_data["list"]:
        date_time = item["dt_txt"]
        date = date_time.split()[0]

        if date not in dates:
            dates.append(date)

    return dates

def get_available_times(forecast_data, selected_date):
    times = []

    for item in forecast_data["list"]:
        date_time = item["dt_txt"]
        date, time = date_time.split()

        if date == selected_date:
            times.append(time)

    return times

def display_selected_forecast(forecast_data, selected_date, selected_time):
    for item in forecast_data["list"]:
        date_time = item["dt_txt"]
        date, time = date_time.split()

        if date == selected_date and time == selected_time:
            temperature = round(int(item["main"]["temp"]) - 273.15, 1)
            condition = item["weather"][0]["description"]
            humidity = item["main"]["humidity"]
            wind_speed = item["wind"]["speed"]

            print("\nSELECTED FORECAST")
            print("-" * 30)
            print(f"Date: {selected_date}")
            print(f"Time: {selected_time}")
            print(f"Temperature: {temperature}°C")
            print(f"Condition: {condition}")
            print(f"Humidity: {humidity}%")
            print(f"Wind Speed: {wind_speed} m/s")

            return

def view_search_history():
    cursor.execute("SELECT * FROM search_history")
    records = cursor.fetchall()

    print("\nSEARCH HISTORY")
    print("-" * 30)

    if len(records) == 0:
        print("No searches found.")
    else:
        for record in records:
            print(f"{record[0]}. {record[1]} - {record[2]}")


#view_search_history()

def get_valid_choice(options, message):
    while True:
        try:
            choice = int(input(message))

            if choice >= 1 and choice <= len(options):
                return choice
            else:
                print("Invalid number. Please choose from the list.")

        except ValueError:
            print("Invalid input. Please enter a number.")

def save_task(task_name, city, task_date, task_time, weather_condition, temperature):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO tasks(task_name, city, task_date, task_time, weather_condition, temperature, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (task_name, city, task_date, task_time, weather_condition, temperature, created_at))

    conn.commit()

    print("Task saved successfully.")

def add_task():
    
    city = input("Enter city for the task: ")

    save_search(city)

    forecast_data = get_forecast(city)

    if forecast_data:
        dates = get_available_dates(forecast_data)

        print("\nAvailable forecast dates:")
        print("-" * 30)

        for index, date in enumerate(dates, start=1):
            print(f"{index}. {date}")

        date_choice = get_valid_choice(dates, "Choose a date number: ")
        selected_date = dates[date_choice - 1]

        times = get_available_times(forecast_data, selected_date)

        print("\nAvailable forecast times:")
        print("-" * 30)

        for index, time in enumerate(times, start=1):
            print(f"{index}. {time}")

        time_choice = get_valid_choice(times, "Choose a time number: ")
        selected_time = times[time_choice - 1]

        for item in forecast_data["list"]:
            date_time = item["dt_txt"]
            date, time = date_time.split()

            if date == selected_date and time == selected_time:
                temperature = round(int(item["main"]["temp"]) - 273.15, 1)
                condition = item["weather"][0]["description"]

                display_selected_forecast(forecast_data, selected_date, selected_time)
                
                task_name = input("Enter task name: ")
                
                save_task(
                    task_name,
                    city,
                    selected_date,
                    selected_time,
                    condition,
                    temperature
                )

                break    

while True:

    print("\n" + "=" * 40)
    print("         WEATHER DASHBOARD")
    print("=" * 40)
    print("1. Check Current Weather")
    print("2. Check Forecast")
    print("3. Add Task")
    print("4. View Search History")
    print("5. Exit")

    choice = input("Choose an option (1-5): ")

    if choice == "1":
        city = input("Enter city: ")
        save_search(city)
        get_current_weather(city)

    elif choice == "2":
        city = input("Enter city: ")
        save_search(city)

        forecast_data = get_forecast(city)

        if forecast_data:
            dates = get_available_dates(forecast_data)

            print("\nAvailable forecast dates:")
            print("-" * 30)

            for index, date in enumerate(dates, start=1):
                print(f"{index}. {date}")

            date_choice = get_valid_choice(dates, "Choose a date number: ")
            selected_date = dates[date_choice - 1]

            print(f"You selected: {selected_date}")  
            
            times = get_available_times(forecast_data, selected_date)

            print("\nAvailable forecast times:")
            print("-" * 30)

            for index, time in enumerate(times, start=1):
                print(f"{index}. {time}")   

            time_choice = get_valid_choice(times, "Choose a time number: ")
            selected_time = times[time_choice - 1]

            print(f"You selected: {selected_time}")  
            display_selected_forecast(forecast_data, selected_date, selected_time)     

    elif choice == "3":
        add_task()

    elif choice == "4":
        view_search_history()

    elif choice == "5":
        print("Thank you for using Weather Dashboard!")
        break

    else:
        print("Invalid choice. Please try again.")
        

conn.close()