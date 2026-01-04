from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import sqlite3
from io import BytesIO
from tensorflow.keras.preprocessing import image
from datetime import datetime

# --------------------------------
# INITIALIZE FLASK APP
# --------------------------------
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# --------------------------------
# HELPER: DB CONNECTION
# --------------------------------
def get_db_connection():
    return sqlite3.connect("pest_system.db")

# --------------------------------
# AUTH API
# --------------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "User already exists"}), 400

    # Insert new user (In production, hash passwords!)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verify user
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful", "username": username})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# --------------------------------
# LOAD TRAINED MODEL
# --------------------------------
# Ensure the model path is correct relative to where you run the script
try:
    model = tf.keras.models.load_model("pest_cnn_model.h5")
except Exception as e:
    print(f"Error loading model: {e}")
    # You might want to handle this gracefully or exit if model is critical

# --------------------------------
# LOAD CLASS NAMES
# --------------------------------
try:
    with open("classes.txt", "r") as f:
        # Assuming format "0 classname" or just "classname"
        # Adjust logic if your classes.txt is just a list of names
        lines = f.readlines()
        if " " in lines[0]:
             class_names = [line.strip().split(" ", 1)[1] for line in lines]
        else:
             class_names = [line.strip() for line in lines]
except Exception as e:
    print(f"Error loading classes: {e}")
    class_names = []

IMG_SIZE = (224, 224)

# --------------------------------
# RISK LEVEL FUNCTION
# --------------------------------
def get_risk_level(confidence):
    if confidence > 80:
        return "High"
    elif confidence > 50:
        return "Medium"
    else:
        return "Low"

# --------------------------------
# HOME ROUTE
# --------------------------------
@app.route("/")
def home():
    return "AI Pest Detection Backend is running"

# --------------------------------
# PREDICT API (AI INFERENCE)
# --------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img_file = request.files["image"]

    try:
        # Image preprocessing using BytesIO to handle standard file upload
        img = image.load_img(BytesIO(img_file.read()), target_size=IMG_SIZE)
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Model prediction
        predictions = model.predict(img_array)
        class_id = int(np.argmax(predictions))
        confidence = float(np.max(predictions) * 100)

        pest_name = class_names[class_id] if class_names else f"Class {class_id}"
        risk_level = get_risk_level(confidence)

        # Store result in DB
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ensure timestamp is recorded
        cursor.execute("""
            INSERT INTO pest_detections (pest_name, confidence, risk_level, timestamp)
            VALUES (?, ?, ?, ?)
        """, (pest_name, round(confidence, 2), risk_level, datetime.now()))

        # Alert Logic
        if risk_level == "High":
             cursor.execute("""
                INSERT INTO alerts (alert_type, message, timestamp)
                VALUES (?, ?, ?)
            """, ("Pest Alert", f"High risk pest detected: {pest_name}", datetime.now()))

        conn.commit()
        conn.close()

        return jsonify({
            "pest_name": pest_name,
            "confidence": round(confidence, 2),
            "risk_level": risk_level
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------------------
# ADD SENSOR DATA API
# --------------------------------
@app.route("/add_sensor", methods=["POST"])
def add_sensor():
    data = request.get_json()

    temperature = data.get("temperature")
    humidity = data.get("humidity")
    soil_moisture = data.get("soil_moisture")

    if temperature is None or humidity is None or soil_moisture is None:
        return jsonify({"error": "Missing sensor data"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sensor_readings (temperature, humidity, soil_moisture, timestamp)
        VALUES (?, ?, ?, ?)
    """, (temperature, humidity, soil_moisture, datetime.now()))

    # Alert Logic
    alert_type = None
    alert_msg = None

    if temperature > 35:
        alert_type = "Temperature Alert"
        alert_msg = "High temperature detected"
    elif soil_moisture < 30:
        alert_type = "Moisture Alert"
        alert_msg = "Low soil moisture detected"

    if alert_type:
        cursor.execute("""
            INSERT INTO alerts (alert_type, message, timestamp)
            VALUES (?, ?, ?)
        """, (alert_type, alert_msg, datetime.now()))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Sensor data stored successfully"
    })

# --------------------------------
# GET HISTORY API
# --------------------------------
@app.route("/api/pests", methods=["GET"])
def get_pests():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Ensure your table has a timestamp column or remove ORDER BY if not
        cursor.execute("SELECT pest_name, confidence, risk_level, timestamp FROM pest_detections ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()

        data = []
        for r in rows:
            data.append({
                "pest_name": r[0],
                "confidence": r[1],
                "risk_level": r[2],
                "timestamp": r[3]
            })
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------------------
# GET ALERTS API
# --------------------------------
@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT alert_type, message, timestamp FROM alerts ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()

        data = []
        for r in rows:
            data.append({
                "alert_type": r[0],
                "message": r[1],
                "timestamp": r[2]
            })
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Host='0.0.0.0' allows external devices (like ESP32) to connect via your IP address
    app.run(host='0.0.0.0', port=5000, debug=True)
