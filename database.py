import sqlite3
from datetime import datetime
DB_NAME = 'data.db'
def connect():
    return sqlite3.connect(DB_NAME)
def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cleanups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        lat REAL,
        lon REAL,
        location_name TEXT,
        photo_file_id TEXT,
        notes TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cleanup_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cleanup_id INTEGER,
        trash_type TEXT,
        weight REAL,
        bags INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trash_spots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        lat REAL,
        lon REAL,
        description TEXT,
        photo_file_id TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()
    def add_user(user_id, username, first_name, last_name):
        conn = connect()
    cur = conn.cursor()
    cur.execute('''
    INSERT OR REPLACE INTO users(id, username, first_name, last_name)
    VALUES (?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name))
    conn.commit()
    conn.close()
    def add_cleanup(user_id, lat, lon, location_name, photo_file_id, notes):
        conn = connect()
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO cleanups(user_id, lat, lon, location_name, photo_file_id, notes, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        lat,
        lon,
        location_name,
        photo_file_id,
        notes,
        datetime.now().strftime('%Y-%m-%d')
    ))

    cleanup_id = cur.lastrowid
    conn.commit()
    conn.close()

    return cleanup_id
def add_cleanup_item(cleanup_id, trash_type, weight, bags):
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO cleanup_items(cleanup_id, trash_type, weight, bags)
    VALUES (?, ?, ?, ?)
    ''', (cleanup_id, trash_type, weight, bags))
    conn.commit()
    conn.close()
    def add_trash_spot(user_id, lat, lon, description, photo_file_id):
        conn = connect()
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO trash_spots(user_id, lat, lon, description, photo_file_id, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        lat,
        lon,
        description,
        photo_file_id,
        datetime.now().strftime('%Y-%m-%d')
    ))
    conn.commit()
    conn.close()
    def get_stats():
        conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT SUM(weight) FROM cleanup_items')
    total_kg = cur.fetchone()[0] or 0
    cur.execute('SELECT COUNT(*) FROM cleanups')
    total_cleanups = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM trash_spots')
    total_spots = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM users')
    total_users = cur.fetchone()[0]
    conn.close()

    return {
        'total_kg': total_kg,
        'total_cleanups': total_cleanups,
        'total_spots': total_spots,
        'total_volunteers': total_users
    }
def get_cleanups():
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
    SELECT c.lat, c.lon, c.location_name, c.created_at,
           u.first_name,
           SUM(ci.weight)
    FROM cleanups c
    LEFT JOIN users u ON c.user_id = u.id
    LEFT JOIN cleanup_items ci ON c.id = ci.cleanup_id
    GROUP BY c.id
    ''')
    rows = cur.fetchall()
    conn.close()
    return [
        {
            'lat': r[0],
            'lon': r[1],
            'location': r[2],
            'date': r[3],
            'volunteer': r[4],
            'weight_kg': r[5]
        }
        for r in rows
    ]
def get_spots():
    conn = connect()
    cur = conn.cursor()

    cur.execute('''
    SELECT lat, lon, description, created_at
    FROM trash_spots
    ''')
    rows = cur.fetchall()
    conn.close()
    return [
        {
            'lat': r[0],
            'lon': r[1],
            'desc': r[2],
            'date': r[3],
            'reporter': 'Пользователь'
        }
        for r in rows
    ]
def get_stats():
    conn = connect()
    cur = conn.cursor()

    cur.execute('SELECT SUM(weight) FROM cleanup_items')
    total_kg = cur.fetchone()[0] or 0

    cur.execute('SELECT COUNT(*) FROM cleanups')
    total_cleanups = cur.fetchone()[0]

    cur.execute('SELECT COUNT(*) FROM trash_spots')
    total_spots = cur.fetchone()[0]

    cur.execute('SELECT COUNT(*) FROM users')
    total_users = cur.fetchone()[0]

    conn.close()

    return {
        'total_kg': total_kg,
        'total_cleanups': total_cleanups,
        'total_spots': total_spots,
        'total_volunteers': total_users
    }
