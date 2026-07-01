# python_capstone_project
# Weather or Not
# A weather-aware daily planning application 
# Problem Definition
People often check weather forecasts before planning their daily activities. However, weather information and daily planning tools are usually provided through separate applications. Users must switch between a weather application to view the forecast and another application to organize their schedules. This separation makes it easy to overlook how changing weather conditions can affect planned activities, leading to inconvenience such as scheduling outdoor activities during rain, forgetting to carry essential items like umbrellas, or missing opportunities to take advantage of favorable weather.
There is a need for a solution that not only provides accurate weather forecasts but also helps users translate that information into practical daily plans. By combining weather forecasts, personalized recommendations, and a planning feature in one application, users can make better-informed decisions about how to organize their day.
The proposed application, Weather or Not, addresses this problem by retrieving real-time weather data, generating weather-based recommendations, and allowing users to create and manage daily plans based on those recommendations. This integration helps users make smarter decisions, improve daily productivity, and adapt their schedules to changing weather conditions from a single application.

# Purpose / Problem Solved
The purpose of Weather or Not is to develop a weather-aware daily planning application that helps users make informed decisions based on current weather conditions and short-term forecasts. The application retrieves real-time weather data, generates practical weather-based recommendations, and enables users to create and manage daily plans that align with the expected weather. By integrating weather forecasting and planning into a single platform, the application helps users organize their activities more efficiently and reduces the need to rely on multiple applications.
From a software development perspective, the project aims to demonstrate the design and implementation of a complete software solution using modern programming concepts and technologies. It integrates an external weather API with a local SQLite database to provide dynamic weather information while storing user plans and preferences. The project applies software engineering principles such as modular programming, database design, CRUD operations, API integration, error handling, and data persistence. 

# Planned Features
The Weather or Not application will include the following features and software components:
Functional Features
•	Search for weather information by entering a city name.
•	Display the current weather conditions.
•	Display today's and tomorrow's weather forecasts.
•	Generate weather-based recommendations to help users plan their day.
•	Allow users to create, view, update, and delete daily plans based on weather recommendations.
•	Save and retrieve user plans from a local SQLite database.
•	Store favorite cities for quick weather searches.
•	Maintain a history of weather searches.
•	Handle invalid city names, API errors, and network connection issues gracefully.

Programming Concepts and Technologies
•	User Input – Accept city names, menu selections, and user plans.
•	Conditional Statements (if/elif/else) – Determine recommendations based on weather conditions and control program flow.
•	Loops (for and while) – Display menus, iterate through forecasts, recommendations, and stored plans.
•	Functions – Organize the application into reusable modules and improve maintainability.
•	Modules – Separate the application into components such as weather retrieval, recommendations, database operations, and user interface.
•	Lists and Dictionaries – Store and process weather data, recommendations, and user information.
•	API Integration – Retrieve real-time weather and forecast data using the OpenWeather API.
•	JSON Processing – Parse and extract relevant information from API responses.
•	SQLite Database – Store user plans, favorite cities, search history, and application preferences.
•	SQL CRUD Operations – Create, Read, Update, and Delete records in the database.
•	Error Handling (try/except) – Handle network failures, invalid user input, and API-related errors.
•	Date and Time Handling – Process forecast dates and organize user plans according to specific days.
•	String Manipulation – Format weather reports, recommendations, and user messages for clear presentation.

# Libraries and Tools
•	Streamlit – to build the graphical user interface (GUI)
•	SQLite3 – for storing user accounts, tasks, notes, events, and expenses
•	Requests – to retrieve weather information from an external API
•	JSON – to parse API responses and store configuration data
•	Datetime – for handling dates, times, deadlines, and scheduled events

# Development Tools
•	Python 3
•	Visual Studio Code (VS Code)
•	Git and GitHub (version control)

# Data Source
The main data source for Weather or Not will be the OpenWeather API. The application will use this API to retrieve real-time weather information and short-term forecast data based on the city entered by the user. The data returned from the API will be in JSON format and will include details such as temperature, weather condition, humidity, wind speed, rainfall information, and forecast times.
In addition to the external weather data, the application will use a local SQLite database to store user-generated data such as daily plans, favorite cities, search history, and user preferences. This allows the application to combine live weather information with stored planning data.

# Success Criteria
The Weather or Not project will be considered successful when it meets the following criteria:
•	Successfully retrieves and displays current weather information for any valid city using the OpenWeather API.
•	Displays accurate weather forecasts for both the current day and the following day.
•	Generates meaningful weather-based recommendations based on the forecast conditions.
•	Allows users to create, view, update, and delete daily plans based on the provided recommendations.
•	Stores and retrieves user plans, favorite cities, and search history using an SQLite database.
•	Handles invalid city names, API failures, and network errors gracefully without crashing.
•	Provides an intuitive and responsive user interface using Streamlit.
•	Organizes the code into modular, reusable components that are easy to maintain and extend.
•	Successfully integrates weather forecasting, recommendations, and daily planning into a single, cohesive application that helps users make informed decisions about their day.










