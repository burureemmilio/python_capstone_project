import streamlit as st
import requests
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Weather Dashboard", layout="wide")

conn = sqlite3.connect("weather.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS search_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    search_time TEXT
)
""")

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

st.title("🌦️ Weather Dashboard")

st.markdown("""
Welcome to your personal weather assistant.

Use the menu on the left to:
- 🌤 Check the current weather
- 📅 View weather forecasts
- 📝 Plan tasks around the weather
- 📖 View your search history
""")

api_key = "dd3d923481948739086ab7bd19423514"

def save_search(city):
    search_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO search_history(city, search_time)
    VALUES (?, ?)
    """, (city, search_time))

    conn.commit()


def get_current_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(url)
    data = response.json()

    if data["cod"] != 200:
        st.error(f"Error: {data['message']}")
        return None

    weather_data = {
        "city": data["name"],
        "temperature": round(float(data["main"]["temp"]) - 273.15, 1),
        "condition": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }

    return weather_data

def get_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"

    response = requests.get(url)
    data = response.json()

    if data["cod"] != "200":
        st.error(f"Error: {data['message']}")
        return None

    return data


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

def save_task(task_name, city, task_date, task_time, weather_condition, temperature):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO tasks(task_name, city, task_date, task_time, weather_condition, temperature, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (task_name, city, task_date, task_time, weather_condition, temperature, created_at))

    conn.commit()

def get_tasks():
    cursor.execute("""
    SELECT id, task_name, city, task_date, task_time, weather_condition, temperature, created_at
    FROM tasks
    ORDER BY id DESC
    """)

    return cursor.fetchall()

def delete_task_by_id(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

    return cursor.rowcount

def update_task_by_id(task_id, task_name, city, task_date, task_time, weather_condition, temperature):
    cursor.execute("""
    UPDATE tasks
    SET task_name = ?, city = ?, task_date = ?, task_time = ?, weather_condition = ?, temperature = ?
    WHERE id = ?
    """, (
        task_name,
        city,
        task_date,
        task_time,
        weather_condition,
        temperature,
        task_id
    ))

    conn.commit()

    return cursor.rowcount

def search_tasks_by_city(city):
    cursor.execute("""
    SELECT id, task_name, city, task_date, task_time, weather_condition, temperature, created_at
    FROM tasks
    WHERE city LIKE ?
    ORDER BY id DESC
    """, (f"%{city}%",))

    return cursor.fetchall()


def get_search_history():
    cursor.execute("""
    SELECT id, city, search_time
    FROM search_history
    ORDER BY id DESC
    """)

    return cursor.fetchall()
menu = st.sidebar.selectbox(
    "Choose an option",
    [
        "Check Current Weather",
        "Check Forecast",
        "Add Task",
        "View Tasks",
        "Delete Task",
        "Update Task",
        "Search Tasks by City",
        "View Search History"
    ]
)

if menu == "Check Current Weather":
    st.header("Check Current Weather")

    city = st.text_input("Enter city")

    if st.button("Check Weather"):
        if city.strip() == "":
            st.warning("Please enter a city.")
        else:
            save_search(city)
            weather = get_current_weather(city)

            if weather:
                st.subheader(f"Weather in {weather['city']}")
                col1, col2, col3 = st.columns(3)

                col1.metric("🌡 Temperature", f"{weather['temperature']}°C")
                col2.metric("💧 Humidity", f"{weather['humidity']}%")
                col3.metric("💨 Wind Speed", f"{weather['wind_speed']} m/s")

                st.success(f"☁ Weather Condition: **{weather['condition'].title()}**")

elif menu == "Check Forecast":
    st.header("Check Weather Forecast")

    city = st.text_input("Enter city")

    if city:
        forecast_data = get_forecast(city)

        if forecast_data:
            save_search(city)

            dates = get_available_dates(forecast_data)
            selected_date = st.selectbox("Select forecast date", dates)

            times = get_available_times(forecast_data, selected_date)
            selected_time = st.selectbox("Select forecast time", times)

            if st.button("Show Forecast"):
                for item in forecast_data["list"]:
                    date, time = item["dt_txt"].split()

                    if date == selected_date and time == selected_time:
                        temperature = round(float(item["main"]["temp"]) - 273.15, 1)
                        condition = item["weather"][0]["description"]
                        humidity = item["main"]["humidity"]
                        wind_speed = item["wind"]["speed"]

                        st.subheader(f"Forecast for {city.title()}")

                        col1, col2, col3 = st.columns(3)

                        col1.metric("🌡 Temperature", f"{temperature}°C")
                        col2.metric("💧 Humidity", f"{humidity}%")
                        col3.metric("💨 Wind Speed", f"{wind_speed} m/s")

                        st.info(f"☁ Weather Condition: **{condition.title()}**")
                        break

elif menu == "Add Task":
    st.header("Add Weather-Based Task")

    city = st.text_input("Enter city for the task")
    task_name = st.text_input("Enter task name")

    if city:
        forecast_data = get_forecast(city)

        if forecast_data:
            dates = get_available_dates(forecast_data)
            selected_date = st.selectbox("Select task date", dates)

            times = get_available_times(forecast_data, selected_date)
            selected_time = st.selectbox("Select task time", times)

            selected_forecast = None

            for item in forecast_data["list"]:
                date, time = item["dt_txt"].split()

                if date == selected_date and time == selected_time:
                    selected_forecast = item
                    break

            if selected_forecast:
                temperature = round(float(selected_forecast["main"]["temp"]) - 273.15, 1)
                condition = selected_forecast["weather"][0]["description"]

                st.subheader("Selected Forecast")
                col1, col2 = st.columns(2)

                col1.metric("🌡 Temperature", f"{temperature}°C")
                col2.info(f"☁ Condition: **{condition.title()}**")

                if st.button("Save Task"):
                    if task_name.strip() == "":
                        st.warning("Please enter a task name.")
                    else:
                        save_search(city)
                        save_task(
                            task_name,
                            city,
                            selected_date,
                            selected_time,
                            condition,
                            temperature
                        )

                        st.success("Task saved successfully.")

elif menu == "View Tasks":
    st.header("Saved Tasks")

    records = get_tasks()

    if len(records) == 0:
        st.info("No tasks found.")
    else:
        st.dataframe(
            records,
            column_config={
                0: "ID",
                1: "Task Name",
                2: "City",
                3: "Date",
                4: "Time",
                5: "Weather",
                6: "Temperature",
                7: "Created At"
            },
            use_container_width=True
        )
elif menu == "Delete Task":
    st.header("Delete Task")

    records = get_tasks()

    if len(records) == 0:
        st.info("No tasks available to delete.")
    else:
        task_options = {}

        for record in records:
            task_id = record[0]
            task_name = record[1]
            city = record[2]
            date = record[3]
            time = record[4]

            task_options[f"{task_id} - {task_name} ({city}, {date} {time})"] = task_id

        selected_task = st.selectbox("Select task to delete", list(task_options.keys()))

        confirm = st.checkbox("I confirm that I want to delete this task")

        if st.button("Delete Task"):
            if not confirm:
                st.warning("Please confirm before deleting.")
            else:
                selected_id = task_options[selected_task]
                deleted = delete_task_by_id(selected_id)

                if deleted > 0:
                    st.success("Task deleted successfully.")
                else:
                    st.error("Task not found.")
elif menu == "Update Task":
    st.header("Update Task")

    records = get_tasks()

    if len(records) == 0:
        st.info("No tasks available to update.")
    else:
        task_options = {}

        for record in records:
            task_id = record[0]
            task_name = record[1]
            city = record[2]
            date = record[3]
            time = record[4]

            task_options[f"{task_id} - {task_name} ({city}, {date} {time})"] = task_id

        selected_task = st.selectbox("Select task to update", list(task_options.keys()))
        selected_id = task_options[selected_task]

        new_task_name = st.text_input("Enter new task name")
        new_city = st.text_input("Enter new city")

        if new_city:
            forecast_data = get_forecast(new_city)

            if forecast_data:
                dates = get_available_dates(forecast_data)
                selected_date = st.selectbox("Select new task date", dates)

                times = get_available_times(forecast_data, selected_date)
                selected_time = st.selectbox("Select new task time", times)

                selected_forecast = None

                for item in forecast_data["list"]:
                    date, time = item["dt_txt"].split()

                    if date == selected_date and time == selected_time:
                        selected_forecast = item
                        break

                if selected_forecast:
                    temperature = round(float(selected_forecast["main"]["temp"]) - 273.15, 1)
                    condition = selected_forecast["weather"][0]["description"]

                    st.subheader("New Selected Forecast")

                    col1, col2 = st.columns(2)
                    col1.metric("🌡 Temperature", f"{temperature}°C")
                    col2.info(f"☁ Condition: **{condition.title()}**")

                    if st.button("Update Task"):
                        if new_task_name.strip() == "":
                            st.warning("Please enter the new task name.")
                        else:
                            updated = update_task_by_id(
                                selected_id,
                                new_task_name,
                                new_city,
                                selected_date,
                                selected_time,
                                condition,
                                temperature
                            )

                            if updated > 0:
                                st.success("Task updated successfully.")
                            else:
                                st.error("Task not found.")

elif menu == "Search Tasks by City":
    st.header("Search Tasks by City")

    city = st.text_input("Enter city to search")

    if st.button("Search"):
        if city.strip() == "":
            st.warning("Please enter a city.")
        else:
            records = search_tasks_by_city(city)

            if len(records) == 0:
                st.info("No tasks found for that city.")
            else:
                st.dataframe(
                    records,
                    column_config={
                        0: "ID",
                        1: "Task Name",
                        2: "City",
                        3: "Date",
                        4: "Time",
                        5: "Weather",
                        6: "Temperature",
                        7: "Created At"
                    },
                    use_container_width=True
                )
elif menu == "View Search History":
    st.header("Search History")

    records = get_search_history()

    if len(records) == 0:
        st.info("No search history found.")
    else:
        st.dataframe(
            records,
            column_config={
                0: "ID",
                1: "City",
                2: "Search Time"
            },
            use_container_width=True
        )