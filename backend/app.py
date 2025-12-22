from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import sqlite3
from tensorflow.keras.preprocessing import image

# --------------------------------
# INITIALIZE FLASK APP
# --------------------------------
app = Flask(__name__)

# --------------------------------
# LOAD TRAINED MODEL
# --------------------------------
model = tf.keras.models.load_model("pest_cnn_model.h5")

# --------------------------------
# LOAD CLASS NAMES
# classes.txt format:
# 0 rice leaf roller
# 1 rice leaf caterpillar
# ...
# --------------------------------
with open("classes.txt", "r") as f:
    class_names = [line.strip().split(" ", 1)[1] for line in f.readlines()]

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
# HOME ROUTE (OPTIONAL)
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

    # Image preprocessing
    img = image.load_img(img_file, target_size=IMG_SIZE)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Model prediction
    predictions = model.predict(img_array)
    class_id = int(np.argmax(predictions))
    confidence = float(np.max(predictions) * 100)

    pest_name = class_names[class_id]
    risk_level = get_risk_level(confidence)

    # --------------------------------
    # STORE AI RESULT
    # --------------------------------
    conn = sqlite3.connect("pest_system.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pest_detections (pest_name, confidence, risk_level)
        VALUES (?, ?, ?)
    """, (pest_name, round(confidence, 2), risk_level))

    # --------------------------------
    # ALERT LOGIC FOR AI PREDICTION
    # --------------------------------
    if confidence > 80:
        cursor.execute("""
            INSERT INTO alerts (message, severity)
            VALUES (?, ?)
        """, (f"High risk pest detected: {pest_name}", "High"))

    conn.commit()
    conn.close()

    return jsonify({
        "pest_name": pest_name,
        "confidence": round(confidence, 2),
        "risk_level": risk_level
    })

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

    conn = sqlite3.connect("pest_system.db")
    cursor = conn.cursor()

    # Store sensor data
    cursor.execute("""
        INSERT INTO sensor_readings (temperature, humidity, soil_moisture)
        VALUES (?, ?, ?)
    """, (temperature, humidity, soil_moisture))

    # --------------------------------
    # ALERT LOGIC FOR SENSOR DATA
    # --------------------------------
    alert_message = None
    severity = "Medium"

    if temperature > 35:
        alert_message = "High temperature detected"
        severity = "High"
    elif humidity > 80:
        alert_message = "High humidity detected"
        severity = "Medium"
    elif soil_moisture < 30:
        alert_message = "Low soil moisture detected"
        severity = "Medium"

    if alert_message:
        cursor.execute("""
            INSERT INTO alerts (message, severity)
            VALUES (?, ?)
        """, (alert_message, severity))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Sensor data stored successfully",
        "temperature": temperature,
        "humidity": humidity,
        "soil_moisture": soil_moisture
    })

# --------------------------------
# RUN SERVER (KEEP THIS LAST)
# --------------------------------
if __name__ == "__main__":
    app.run(debug=True)
