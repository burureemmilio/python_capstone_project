from datetime import datetime
from database import get_connection


def save_task(task_name, city, task_date, task_time, weather_condition, temperature):
    conn = get_connection()
    cursor = conn.cursor()

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO tasks(task_name, city, task_date, task_time, weather_condition, temperature, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (task_name, city, task_date, task_time, weather_condition, temperature, created_at))

    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, task_name, city, task_date, task_time, weather_condition, temperature, created_at
    FROM tasks
    ORDER BY id DESC
    """)

    tasks = cursor.fetchall()
    conn.close()

    return tasks


def delete_task_by_id(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

    deleted = cursor.rowcount
    conn.close()

    return deleted


def update_task_by_id(task_id, task_name, city, task_date, task_time, weather_condition, temperature):
    conn = get_connection()
    cursor = conn.cursor()

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

    updated = cursor.rowcount
    conn.close()

    return updated


def search_tasks_by_city(city):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, task_name, city, task_date, task_time, weather_condition, temperature, created_at
    FROM tasks
    WHERE city LIKE ?
    ORDER BY id DESC
    """, (f"%{city}%",))

    results = cursor.fetchall()
    conn.close()

    return results