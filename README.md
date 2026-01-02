 

***

```markdown
# 🌱 AI-Based Pest Detection and Monitoring System 🐛

AI-powered pest detection and monitoring system using **CNN**, **Flask**, **SQLite**, and a **web dashboard**.

---

## 📘 Overview

This project is an AI and IoT-based smart agriculture system designed to detect crop pests from images and monitor environmental conditions such as temperature, humidity, and soil moisture. The system integrates **deep learning**, **IoT**, and a **web-based dashboard** to assist farmers in early pest detection and effective crop management.

---

## 🚀 Project Features

- 🧠 AI-based pest classification using a Convolutional Neural Network (CNN)
- 🪲 Image-based pest detection with confidence score and risk level
- 🌡️ Real-time environmental monitoring using IoT sensors
- 🔔 Automatic alert generation for high-risk pest and abnormal sensor values
- 📊 Responsive web dashboard for visualization and monitoring
- ☁️ Scalable architecture supporting both simulated and real IoT data

---

## 🧠 Technologies Used

### 🔹 AI & Backend
- Python  
- TensorFlow / Keras  
- Flask (REST API)  
- SQLite Database  

### 🔹 IoT
- ESP32 Development Board  
- DHT11 / DHT22 (Temperature & Humidity Sensor)  
- Soil Moisture Sensor  
- HTTP-based communication  

### 🔹 Frontend
- HTML5  
- Bootstrap 5  
- JavaScript (Fetch API)  

---

## 📂 Project Structure

```
AI-Pest-Detection/
│
├── app.py                # Flask backend (AI inference + APIs)
├── database.py           # Database setup
├── pest_cnn_model.h5     # Trained CNN model
├── classes.txt           # Pest class labels
├── pest_system.db        # SQLite database
│
├── train_cnn.py          # Model training script
├── test_cnn.py           # Model testing script
├── load_dataset.py       # Dataset loader
│
├── classification/       # Dataset (train/val/test)
│
├── frontend/
│   ├── index.html        # Dashboard
│   ├── history.html      # Pest detection history
│   ├── alerts.html       # Alerts page
│   ├── reports.html      # Reports page
│   ├── login.html        # Login UI
│   ├── api.js            # Frontend API calls
│   └── styles.css        # Common styling
│
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## ⚙️ How to Run the Project

### 1️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows:**
```bash
.\.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Initialize Database

```bash
python database.py
```

### 4️⃣ Start Backend Server

```bash
python app.py
```

Server runs at:  
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 5️⃣ Open Web Dashboard

Open in browser:  
`frontend/login.html`

Navigate using the dashboard menu.

---

## 🔌 IoT Integration

Sensor data is sent to the backend via:

```http
POST /add_sensor
```

**JSON format:**

```json
{
  "temperature": 35,
  "humidity": 70,
  "soil_moisture": 28
}
```

The system supports both:
- Simulated sensor data  
- Real IoT devices (ESP32)

---

## 🚨 Alert Logic

Alerts are automatically generated when:

- Pest confidence > 80% → 🪲 **Pest Alert**
- Temperature > 35°C → 🌡️ **Heat Alert**
- Soil moisture < 30% → 💧 **Drought Alert**

---

## 📈 Future Enhancements

- CSV / PDF report export  
- MQTT-based real-time IoT communication  
- Multi-node sensor deployment  
- Automated irrigation or pesticide control  

---

## 👨‍💻 Author

**Aaryan**  
B.E. Information Science Engineering  

**GitHub:**  
[https://github.com/AARYAN-5-14/ai-based-pest-detection-and-monitoring](https://github.com/AARYAN-5-14/ai-based-pest-detection-and-monitoring)
```



