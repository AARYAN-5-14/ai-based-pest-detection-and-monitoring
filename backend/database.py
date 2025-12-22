import sqlite3

conn = sqlite3.connect("pest_system.db")
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

# Pest detections table
cursor.execute("""
CREATE TABLE IF NOT EXISTS pest_detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pest_name TEXT,
    confidence REAL,
    risk_level TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Sensor readings table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL,
    humidity REAL,
    soil_moisture REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Alerts table
cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    severity TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ Database and tables created successfully")
