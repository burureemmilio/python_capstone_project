import streamlit as st
import pandas as pd

from database import create_tables, save_search, get_search_history
from weather import (
    get_current_weather,
    get_forecast,
    get_available_dates,
    get_available_times,
    get_selected_forecast,
    get_weather_advice
)
from tasks import (
    save_task,
    get_tasks,
    delete_task_by_id,
    update_task_by_id,
    search_tasks_by_city
)

st.set_page_config(page_title="Weather Dashboard", layout="wide")

create_tables()

st.title("🌦️ Weather Dashboard")

st.markdown("""
Welcome to your personal weather assistant.

Use the menu on the left to:
- 🌤 Check the current weather
- 📅 View weather forecasts
- 📝 Plan tasks around the weather
- 📖 View your search history
""")
st.sidebar.title("Menu")

menu = st.sidebar.radio(
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
            weather, error = get_current_weather(city)

            if error:
                st.error(error)
            else:
                save_search(city)

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
        forecast_data, error = get_forecast(city)

        if error:
            st.error(error)
        else:
            dates = get_available_dates(forecast_data)
            selected_date = st.selectbox("Select forecast date", dates)

            times = get_available_times(forecast_data, selected_date)
            selected_time = st.selectbox("Select forecast time", times)

            if st.button("Show Forecast"):
                selected_forecast = get_selected_forecast(
                    forecast_data,
                    selected_date,
                    selected_time
                )

                if selected_forecast:
                    save_search(city)

                    st.subheader(f"Forecast for {city.title()}")

                    col1, col2, col3 = st.columns(3)

                    col1.metric("🌡 Temperature", f"{selected_forecast['temperature']}°C")
                    col2.metric("💧 Humidity", f"{selected_forecast['humidity']}%")
                    col3.metric("💨 Wind Speed", f"{selected_forecast['wind_speed']} m/s")

                    st.info(f"☁ Weather Condition: **{selected_forecast['condition'].title()}**")


elif menu == "Add Task":
    st.header("Add Weather-Based Task")

    city = st.text_input("Enter city for the task")

    if city:
        forecast_data, error = get_forecast(city)

        if error:
            st.error(error)
        else:
            dates = get_available_dates(forecast_data)
            selected_date = st.selectbox("Select task date", dates)

            times = get_available_times(forecast_data, selected_date)
            selected_time = st.selectbox("Select task time", times)

            selected_forecast = get_selected_forecast(
                forecast_data,
                selected_date,
                selected_time
            )

            task_name = st.text_input("Enter task name")
             
            advice = get_weather_advice(selected_forecast["condition"])
            st.warning(f"Advice: {advice}")
            if selected_forecast:
                st.subheader("Selected Forecast")

                col1, col2 = st.columns(2)

                col1.metric("🌡 Temperature", f"{selected_forecast['temperature']}°C")
                col2.info(f"☁ Condition: **{selected_forecast['condition'].title()}**")

                confirm_task = st.checkbox("I confirm that I want to save this task")

                if st.button("Save Task"):
                    if task_name.strip() == "":
                        st.warning("Please enter a task name.")
                    elif not confirm_task:
                        st.warning("Please confirm before saving.")
                    else:
                        save_search(city)

                        save_task(
                            task_name,
                            city,
                            selected_date,
                            selected_time,
                            selected_forecast["condition"],
                            selected_forecast["temperature"]
                        )

                        st.success("Task saved successfully.")
                       
                if st.button("Discard Task"):
                    st.info("Task discarded. It was not saved.")


elif menu == "View Tasks":
    st.header("Saved Tasks")

    records = get_tasks()

    if len(records) == 0:
        st.info("No tasks found.")
    else:
        df = pd.DataFrame(records, columns=[
            "ID",
            "Task Name",
            "City",
            "Date",
            "Time",
            "Weather",
            "Temperature",
            "Created At"
        ])

        st.dataframe(df, use_container_width=True)


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
            forecast_data, error = get_forecast(new_city)

            if error:
                st.error(error)
            else:
                dates = get_available_dates(forecast_data)
                selected_date = st.selectbox("Select new task date", dates)

                times = get_available_times(forecast_data, selected_date)
                selected_time = st.selectbox("Select new task time", times)

                selected_forecast = get_selected_forecast(
                    forecast_data,
                    selected_date,
                    selected_time
                )

                if selected_forecast:
                    advice = get_weather_advice(selected_forecast["condition"])
                    st.warning(f"Advice: {advice}")
                    st.subheader("New Selected Forecast")

                    col1, col2 = st.columns(2)

                    col1.metric("🌡 Temperature", f"{selected_forecast['temperature']}°C")
                    col2.info(f"☁ Condition: **{selected_forecast['condition'].title()}**")

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
                                selected_forecast["condition"],
                                selected_forecast["temperature"]
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
                df = pd.DataFrame(records, columns=[
                    "ID",
                    "Task Name",
                    "City",
                    "Date",
                    "Time",
                    "Weather",
                    "Temperature",
                    "Created At"
                ])

                st.dataframe(df, use_container_width=True)


elif menu == "View Search History":
    st.header("Search History")

    records = get_search_history()

    if len(records) == 0:
        st.info("No search history found.")
    else:
        df = pd.DataFrame(records, columns=[
            "ID",
            "City",
            "Search Time"
        ])

        st.dataframe(df, use_container_width=True)