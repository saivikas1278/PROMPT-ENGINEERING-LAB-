import sqlite3
import os

DB_NAME = 'transport.db'
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create routes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_number TEXT NOT NULL,
        source TEXT NOT NULL,
        destination TEXT NOT NULL,
        distance REAL NOT NULL,
        travel_time INTEGER NOT NULL,
        fare REAL NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

def insert_sample_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute('SELECT COUNT(*) FROM routes')
    count = cursor.fetchone()[0]
    
    if count == 0:
        sample_routes = [
            ('101', 'SRKR Engineering College', 'Bhimavaram Bus Stand', 8, 25, 20),
            ('102', 'SRKR Engineering College', 'Bhimavaram Bus Stand', 9, 30, 25),
            ('105', 'SRKR Engineering College', 'Bhimavaram Bus Stand', 10, 35, 15),
            ('201', 'SRKR Engineering College', 'Bhimavaram Railway Station', 7, 20, 15),
            ('202', 'SRKR Engineering College', 'Bhimavaram Railway Station', 7.5, 22, 20),
            ('301', 'SRKR Engineering College', 'Undi', 12, 40, 30),
            ('401', 'Bhimavaram', 'Eluru', 60, 90, 80),
            ('402', 'Bhimavaram', 'Eluru', 65, 100, 70),
            ('501', 'Bhimavaram', 'Akividu', 20, 45, 40),
            ('502', 'Bhimavaram', 'Akividu', 22, 50, 35)
        ]
        
        cursor.executemany('''
        INSERT INTO routes (bus_number, source, destination, distance, travel_time, fare)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_routes)
        
        conn.commit()
        
    conn.close()

def get_all_routes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM routes ORDER BY id DESC')
    routes = cursor.fetchall()
    conn.close()
    return routes

def get_route_by_id(route_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM routes WHERE id = ?', (route_id,))
    route = cursor.fetchone()
    conn.close()
    return route

def get_locations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT source as location FROM routes
        UNION
        SELECT destination as location FROM routes
        ORDER BY location
    ''')
    locations = [row['location'] for row in cursor.fetchall()]
    conn.close()
    return locations

def search_routes(source, destination):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM routes
        WHERE source = ? AND destination = ?
    ''', (source, destination))
    routes = cursor.fetchall()
    conn.close()
    return routes

def add_route(bus_number, source, destination, distance, travel_time, fare):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO routes (bus_number, source, destination, distance, travel_time, fare)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (bus_number, source, destination, distance, travel_time, fare))
    conn.commit()
    conn.close()

def update_route(route_id, bus_number, source, destination, distance, travel_time, fare):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE routes
        SET bus_number = ?, source = ?, destination = ?, distance = ?, travel_time = ?, fare = ?
        WHERE id = ?
    ''', (bus_number, source, destination, distance, travel_time, fare, route_id))
    conn.commit()
    conn.close()

def delete_route(route_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM routes WHERE id = ?', (route_id,))
    conn.commit()
    conn.close()
