import sqlite3
import os
import time
import hashlib

DB_PATH = "data/care.db"

def get_connection():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def _hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            room TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'online',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            age INTEGER,
            room TEXT NOT NULL,
            device_id INTEGER,
            status TEXT NOT NULL DEFAULT 'All Good',
            is_live INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (device_id) REFERENCES devices (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            device_id INTEGER,
            timestamp TEXT NOT NULL,
            confidence REAL,
            priority TEXT NOT NULL DEFAULT 'High',
            resolved INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (person_id) REFERENCES persons (id),
            FOREIGN KEY (device_id) REFERENCES devices (id)
        )
    """)

    conn.commit()

    # Migration: add motionless_seconds column for databases created before
    # this setting existed (ALTER fails silently if the column already exists)
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN motionless_seconds INTEGER NOT NULL DEFAULT 10")
        conn.commit()
    except sqlite3.OperationalError:
        pass

    conn.close()

def add_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (username, email, _hash_password(password), time.strftime("%Y-%m-%d %H:%M:%S"))
        )
        user_id = cursor.lastrowid
        conn.commit()
        success = user_id
    except sqlite3.IntegrityError:
        success = None
    conn.close()
    return success

def verify_user(username, password):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row and row["password_hash"] == _hash_password(password):
        return dict(row)
    return None

def get_user_by_username(username):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_device(user_id, room, status="online"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO devices (user_id, room, status) VALUES (?, ?, ?)", (user_id, room, status))
    device_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return device_id

def get_devices(user_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices WHERE user_id = ?", (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def delete_device(device_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM devices WHERE id = ? AND user_id = ?", (device_id, user_id))
    conn.commit()
    conn.close()

def add_person(user_id, name, age, room, device_id, is_live=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO persons (user_id, name, age, room, device_id, status, is_live) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, name, age, room, device_id, "All Good", is_live)
    )
    person_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return person_id

def get_persons(user_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM persons WHERE user_id = ?", (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_person_by_id(person_id, user_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM persons WHERE id = ? AND user_id = ?", (person_id, user_id))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_live_person(user_id=None, username=None):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if username and not user_id:
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        u = cursor.fetchone()
        if not u:
            conn.close()
            return None
        user_id = u["id"]
    cursor.execute("SELECT * FROM persons WHERE user_id = ? AND is_live = 1 LIMIT 1", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def delete_person(person_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alerts WHERE person_id = ?", (person_id,))
    cursor.execute("DELETE FROM persons WHERE id = ? AND user_id = ?", (person_id, user_id))
    conn.commit()
    conn.close()

def set_person_status(person_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE persons SET status = ? WHERE id = ?", (status, person_id))
    conn.commit()
    conn.close()

def log_alert(person_id, device_id, confidence, priority="High", timestamp=None):
    conn = get_connection()
    cursor = conn.cursor()
    ts = timestamp or time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO alerts (person_id, device_id, timestamp, confidence, priority, resolved) VALUES (?, ?, ?, ?, ?, 0)",
        (person_id, device_id, ts, confidence, priority)
    )
    alert_id = cursor.lastrowid
    conn.commit()
    conn.close()
    set_person_status(person_id, "Fall Detected")
    return alert_id

def get_alerts(user_id, limit=None):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
        SELECT alerts.*, persons.name AS person_name, persons.room AS room
        FROM alerts
        JOIN persons ON alerts.person_id = persons.id
        WHERE persons.user_id = ?
        ORDER BY alerts.timestamp DESC
    """
    if limit:
        query += f" LIMIT {int(limit)}"
    cursor.execute(query, (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_alert_by_id(alert_id, user_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT alerts.*, persons.name AS person_name, persons.age AS age, persons.room AS room
        FROM alerts
        JOIN persons ON alerts.person_id = persons.id
        WHERE alerts.id = ? AND persons.user_id = ?
    """, (alert_id, user_id))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def resolve_alert(alert_id, person_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE alerts SET resolved = 1 WHERE id = ?", (alert_id,))
    conn.commit()
    conn.close()
    set_person_status(person_id, "All Good")

def get_active_alert_count(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM alerts
        JOIN persons ON alerts.person_id = persons.id
        WHERE persons.user_id = ? AND alerts.resolved = 0
    """, (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_total_falls_this_month(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    month = time.strftime("%Y-%m")
    cursor.execute("""
        SELECT COUNT(*) FROM alerts
        JOIN persons ON alerts.person_id = persons.id
        WHERE persons.user_id = ? AND alerts.timestamp LIKE ?
    """, (user_id, f"{month}%"))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_fall_counts_by_day(user_id, days=30):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT substr(alerts.timestamp, 1, 10) AS day, COUNT(*) AS count
        FROM alerts
        JOIN persons ON alerts.person_id = persons.id
        WHERE persons.user_id = ?
        GROUP BY day
        ORDER BY day ASC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def clear_live_person(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE persons SET is_live = 0 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_motionless_seconds(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT motionless_seconds FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row and row[0] is not None else 10

def update_motionless_seconds(user_id, seconds):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET motionless_seconds = ? WHERE id = ?", (int(seconds), user_id))
    conn.commit()
    conn.close()