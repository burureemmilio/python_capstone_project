from datetime import datetime
from database import cursor, conn


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