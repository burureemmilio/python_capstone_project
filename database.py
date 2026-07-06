import sqlite3
from datetime import datetime


def get_connection():
    return sqlite3.connect("weather.db")


def create_tables():
    conn = get_connection()
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
    conn.close()


def save_search(city):
    conn = get_connection()
    cursor = conn.cursor()

    search_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO search_history(city, search_time)
    VALUES (?, ?)
    """, (city, search_time))

    conn.commit()
    conn.close()


def get_search_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, city, search_time
    FROM search_history
    ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records