# Real-Time Sensor Data Processing with FastAPI, MQTT, and MySQL

## 📌 Project Overview
This project is a **FastAPI-based service** that continuously listens to multiple MQTT topics, ingests sensor data in real-time, and stores it into a **MySQL database**.  
It also checks incoming values against predefined **threshold conditions**, and whenever a threshold is breached, an **alert** is generated and stored in a separate table.

This project was developed as part of an **assessment task**.

---

## 🚀 Features
- MQTT subscriber listens to **5–10 topics** (e.g., `sensors/data1`, `sensors/data2`, etc.).
- Each message is a **JSON object** with **5 key-value pairs**:
  - `temperature`
  - `humidity`
  - `voltage`
  - `pressure`
  - `light`
- **Threshold monitoring**:
  - If a value exceeds its threshold → log an **alert**.
- **MySQL database integration**:
  - Raw data stored in `raw_data` table.
  - Alerts stored in `alerts` table.
- **FastAPI endpoints**:
  - `GET /` → Root check
  - `POST /raw_data` → Insert raw data manually
  - `GET /raw_data` → Retrieve stored raw data
  - `POST /alert` → Insert alert manually
  - `GET /alert` → Retrieve stored alerts
- **Dockerized setup** with:
  - FastAPI app
  - MySQL database
  - MQTT broker (Eclipse Mosquitto)
  - Data simulator (publishes random sensor data)

---

## 🗄️ Database Schema

### `raw_data` table
| Column      | Type        | Description                   |
|-------------|------------|-------------------------------|
| id          | INT (PK)   | Auto-increment record ID       |
| temperature | FLOAT      | Temperature value              |
| humidity    | FLOAT      | Humidity value                 |
| voltage     | FLOAT      | Voltage value                  |
| pressure    | FLOAT      | Pressure value                 |
| light       | FLOAT      | Light intensity value          |
| raw_json    | JSON/Text  | Original message payload       |
| timestamp   | DATETIME   | Record timestamp               |

### `alerts` table
| Column     | Type        | Description                         |
|------------|------------|-------------------------------------|
| id         | INT (PK)   | Auto-increment alert ID              |
| raw_id     | INT (FK)   | Reference to `raw_data.id`           |
| key        | VARCHAR    | Key that violated threshold          |
| value      | FLOAT      | Actual value received                |
| threshold  | FLOAT      | Defined threshold value              |
| timestamp  | DATETIME   | Alert trigger time                   |

---

## ⚙️ Tech Stack
- **FastAPI** (Python 3.10+)
- **Paho-MQTT** (MQTT client)
- **SQLAlchemy** (ORM for MySQL)
- **MySQL** (Relational Database)
- **Eclipse Mosquitto** (MQTT Broker)
- **Docker & Docker Compose**

---

## 🛠️ Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/your-username/real_time_backend.git
cd real_time_backend
