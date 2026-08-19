import sys
import os
import shutil
import sqlite3
import pickle

import numpy as np
import pandas as pd
from ai.alert_engine import evaluate_alert
from database.alerts import (
    create_alert_table,
    save_alert,
    get_alerts
)
# ==========================================
# AI Explanation Generator
# ==========================================

def generate_explanation(
    probability,
    severity,
    status
):

    explanation = []


    if probability >= 70:

        explanation.append(
            "High leakage probability detected"
        )

        explanation.append(
            "Sensor pattern shows abnormal behavior"
        )


    elif probability >= 30:

        explanation.append(
            "Moderate risk detected"
        )

        explanation.append(
            "Continuous monitoring recommended"
        )


    else:

        explanation.append(
            "Sensor values are within normal range"
        )

        explanation.append(
            "No significant leakage pattern detected"
        )


    explanation.append(
        f"Risk classification: {severity}"
    )


    explanation.append(
        f"AI decision: {status}"
    )


    return explanation

from datetime import datetime

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
class SensorInput(BaseModel):

    flow_rate: float

    pressure: float

    temperature: float

# ==========================================
# Add src path
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SRC_DIR = os.path.join(
    BASE_DIR,
    "src"
)

if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)


# ==========================================
# Project Imports
# ==========================================

from features.advanced_features import (
    extract_advanced_features
)

from ml.anomaly_detector import (
    detect_anomaly
)

from app.sensor import (
    generate_sensor_data
)

# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI(
    title="Smart Water Leakage AI",
    description="AI based Smart Water Leakage Detection System",
    version="1.0.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


# ==========================================
# Paths
# ==========================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "leakage_detector_rf.pkl"
)

DB_PATH = os.path.join(
    BASE_DIR,
    "data",
    "leakage_history.db"
)

TEMP_FILE = os.path.join(
    BASE_DIR,
    "temp_sensor.csv"
)


# ==========================================
# Optimized Leakage Threshold
# ==========================================

# Threshold analysis:
#
# 0.30 produced:
#
# Precision = 80.82%
# Recall    = 92.19%
# F1        = 86.13%
#
# Therefore we use 0.30.

LEAKAGE_THRESHOLD = 0.30


# ==========================================
# Load ML Model
# ==========================================

if not os.path.exists(MODEL_PATH):

    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )


with open(
    MODEL_PATH,
    "rb"
) as file:

    model = pickle.load(file)
# ==========================================
# Latest Live Alert State
# ==========================================

latest_alert_status = {
    "alert": False,
    "message": "System Normal",
    "probability": 0.0,
    "severity": "LOW",
    "timestamp": None,
    "threshold": LEAKAGE_THRESHOLD * 100
}

# ==========================================
# Database Initialization
# ==========================================

def create_database():

    os.makedirs(
        os.path.dirname(DB_PATH),
        exist_ok=True
    )

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            status TEXT,
            probability REAL,
            severity TEXT,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flow_rate REAL,
            pressure REAL,
            temperature REAL,
            status TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


create_database()
create_alert_table()
# ==========================================
# Severity
# ==========================================

def get_severity(
    probability: float
):

    probability = float(
        probability
    )

    if probability < 0.30:

        return "LOW"

    elif probability < 0.60:

        return "MEDIUM"

    else:

        return "HIGH"


# ==========================================
# Leakage Status
# ==========================================

def get_leakage_status(
    probability: float
):

    probability = float(
        probability
    )

    if probability >= LEAKAGE_THRESHOLD:

        return "Leakage Detected"

    return "Normal"


# ==========================================
# Home API
# ==========================================

@app.get("/")
def home():

    return {

        "message":
        "Smart Water Leakage AI API Running",

        "version":
        "1.0.0",

        "leakage_threshold":
        float(LEAKAGE_THRESHOLD),

        "leakage_threshold_percent":
        float(
            LEAKAGE_THRESHOLD * 100
        )

    }


# ==========================================
# CSV Prediction
# ==========================================

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):

    try:

        # ==================================
        # Save Uploaded File
        # ==================================

        with open(
            TEMP_FILE,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        # ==================================
        # Read CSV
        # ==================================

        df = pd.read_csv(
            TEMP_FILE
        )


        # ==================================
        # Validate CSV
        # ==================================

        if "Value" not in df.columns:

            return {

                "error":
                "CSV must contain a 'Value' column"

            }


        signal = df[
            "Value"
        ].dropna().values


        if len(signal) == 0:

            return {

                "error":
                "CSV contains no valid sensor values"

            }


        # ==================================
        # Anomaly Detection
        # ==================================

        try:

            anomaly_result = detect_anomaly(
                signal
            )

        except Exception as error:

            anomaly_result = {

                "status":
                "Unavailable",

                "message":
                str(error)

            }


        # ==================================
        # Feature Extraction
        # ==================================

        features = extract_advanced_features(
            signal
        )


        feature_df = pd.DataFrame(
            [features]
        )


        # ==================================
        # ML Prediction
        # ==================================

        raw_probability = model.predict_proba(
            feature_df
        )[0][1]


        # Force Python float
        probability_decimal = float(
            raw_probability
        )


        probability = round(
            probability_decimal * 100,
            2
        )


        # ==================================
        # Leakage Decision
        # ==================================

        status = get_leakage_status(
            probability_decimal
        )


        severity = get_severity(
            probability_decimal
        )
        
        explanation = generate_explanation(
            probability,
            severity,
            status
        )
        # ==================================
        # Anomaly Detection
        # ==================================

     


        # ==================================
        # Save Prediction History
        # ==================================

        conn = sqlite3.connect(
            DB_PATH
        )

        cursor = conn.cursor()


        cursor.execute(
            """
            INSERT INTO history
            (
                filename,
                status,
                probability,
                severity,
                timestamp
            )

            VALUES (?, ?, ?, ?, ?)
            """,
            (
                file.filename,

                status,

                float(probability),

                severity,

                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )


        conn.commit()

        conn.close()


        # ==================================
        # Response
        # ==================================

        return {

            "status":
            status,

            "leakage_probability":
            float(probability),

            "severity":
            severity,

            "threshold":
            float(
                LEAKAGE_THRESHOLD * 100
            ),

            "signal":
            [
                float(value)
                for value in signal[:500]
            ],

            "anomaly":
            anomaly_result,

            "saved":
            True

        }


    except Exception as error:

        return {

            "error":
            str(error)

        }


    finally:

        if os.path.exists(
            TEMP_FILE
        ):

            os.remove(
                TEMP_FILE
            )


# ==========================================
# Prediction History
# ==========================================

@app.get("/history")
def history():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            filename,
            status,
            probability,
            severity,
            timestamp

        FROM history

        ORDER BY id DESC
        """
    )


    rows = cursor.fetchall()

    conn.close()


    result = []


    for row in rows:

        result.append(

            {

                "filename":
                str(row[0]),

                "status":
                str(row[1]),

                "probability":
                float(row[2]),

                "severity":
                str(row[3]),

                "timestamp":
                str(row[4])

            }

        )


    return result


# ==========================================
# Live Sensor
# ==========================================

@app.get("/sensor/live")
def live_sensor():

    data = generate_sensor_data()
    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO sensor_data
        (
            flow_rate,
            pressure,
            temperature,
            status,
            timestamp
        )

        VALUES (?, ?, ?, ?, ?)
        """,

        (
            data["flow_rate"],
            data["pressure"],
            data["temperature"],
            data["status"],
            data["timestamp"]
        )
    )


    conn.commit()

    conn.close()

    return {

        "timestamp":
        str(data["timestamp"]),

        "flow_rate":
        float(data["flow_rate"]),

        "pressure":
        float(data["pressure"]),

        "temperature":
        float(data["temperature"]),

        "status":
        str(data["status"])

    }
# ==========================================
# Sensor History
# ==========================================

@app.get("/sensor/history")
def sensor_history():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            flow_rate,
            pressure,
            temperature,
            status,
            timestamp

        FROM sensor_data

        ORDER BY id DESC

        LIMIT 100
        """
    )


    rows = cursor.fetchall()

    conn.close()


    result = []


    for row in rows:

        result.append(

            {
                "flow_rate": float(row[0]),

                "pressure": float(row[1]),

                "temperature": float(row[2]),

                "status": row[3],

                "timestamp": row[4]

            }

        )


    return result

# ==========================================
# Live Sensor Prediction
# ==========================================

@app.post("/sensor/predict")
def sensor_predict(
    data: SensorInput
):

    # ==================================
    # Read Sensor Values
    # ==================================

    flow_rate = data.flow_rate
    pressure = data.pressure
    temperature = data.temperature
    # ==================================
    # Create Sensor Signal
    # ==================================

    signal = np.array(

        [

            flow_rate,

            pressure,

            temperature

        ],

        dtype=float

    )


    # Model expects a signal-like input
    signal = np.resize(
        signal,
        500
    )


    # ==================================
    # Feature Extraction
    # ==================================

    features = extract_advanced_features(
        signal
    )


    feature_df = pd.DataFrame(
        [features]
    )


    # ==================================
    # Prediction
    # ==================================

    raw_probability = model.predict_proba(
        feature_df
    )[0][1]


    probability_decimal = float(
        raw_probability
    )


    probability = round(
        probability_decimal * 100,
        2
    )
    


    # ==================================
    # Leakage Decision
    # ==================================

    status = get_leakage_status(
        probability_decimal
    )


    severity = get_severity(
        probability_decimal
    )
    # ==========================================
    # False Alarm Reduction
    # ==========================================

    global latest_alert_status
    global consecutive_leakage_count

    if probability_decimal >= LEAKAGE_THRESHOLD:

        consecutive_leakage_count += 1

    else:

        consecutive_leakage_count = 0


    confirmed_alert = (
        consecutive_leakage_count
        >= LEAK_CONFIRMATION_COUNT
    )


    if confirmed_alert:

        alert_message = "🚨 Water Leakage Confirmed"

    else:

        alert_message = "✅ System Normal"


    # ==========================================
    # Update Current Alert State
    # ==========================================

    latest_alert_status = {

        "alert": bool(confirmed_alert),

        "message": alert_message,

        "probability": float(probability),

        "severity": str(severity),

        "timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "threshold":
            float(
                LEAKAGE_THRESHOLD * 100
            ),

        "confirmation_count":
            consecutive_leakage_count,

        "required_confirmations":
            LEAK_CONFIRMATION_COUNT
    }


    explanation = generate_explanation(
        probability,
        severity,
        status
    )
    # ==================================
    # Anomaly Detection
    # ==================================

    try:

        anomaly_result = detect_anomaly(
            signal
        )

    except Exception as error:

        anomaly_result = {

            "status": "Unavailable",

            "score": 0,

            "count": 0,

            "message": str(error)

        }
  
    # ==================================
    # Save Live Prediction History
    # Only save high risk events
    # ==================================

    if probability_decimal >= 0.60:



        conn = sqlite3.connect(
            DB_PATH
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO history
            (
                filename,
                status,
                probability,
                severity,
                timestamp
            )

            VALUES (?, ?, ?, ?, ?)
            """,

            (
                "LIVE_SENSOR",
                status,
                float(probability),
                severity,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

        )

        conn.commit()

        conn.close()
    # ==========================================
    # Smart Alert Engine
    # ==========================================

    alert_result = evaluate_alert(
        probability=probability,
        pressure=pressure,
        flow_rate=flow_rate
    )


    # ==========================================
    # Save Alert Only When Both Confirm
    # ==========================================

    if (
        alert_result["alert"]
        and confirmed_alert
    ):

        save_alert(
            "Leakage Detection",
            alert_result["message"],
            alert_result["severity"],
            probability
        )   
    # ==================================
    # Response
    # ==================================

    return {

        "status": status,

        "leakage_probability":
            float(probability),

        "severity":
            severity,

        "explanation":
            explanation,

        "anomaly":
            anomaly_result,

        "threshold":
            float(
                LEAKAGE_THRESHOLD * 100
            ),

        "sensor_data": {

            "flow_rate":
                flow_rate,

            "pressure":
                pressure,

            "temperature":
                temperature
        }

    }


# ==========================================
# Alert History
# ==========================================

@app.get("/alerts")
def alerts():

    return get_alerts()

# ==========================================
# Dashboard Statistics
# ==========================================

@app.get("/stats")
def stats():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()


    # Total predictions

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM history
        """
    )

    total_predictions = cursor.fetchone()[0]



    # Leakage count

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM history
        WHERE status='Leakage Detected'
        """
    )

    leakage_detected = cursor.fetchone()[0]



    # Normal count

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM history
        WHERE status='Normal'
        """
    )

    normal_cases = cursor.fetchone()[0]



    # Average probability

    cursor.execute(
        """
        SELECT AVG(probability)
        FROM history
        """
    )

    avg_probability = cursor.fetchone()[0]


    if avg_probability is None:

        avg_probability = 0



    # Severity Analysis

    cursor.execute(
        """
        SELECT severity, COUNT(*)
        FROM history
        GROUP BY severity
        """
    )


    severity_rows = cursor.fetchall()



    severity_count = {

        "LOW":0,

        "MEDIUM":0,

        "HIGH":0

    }



    for row in severity_rows:

        severity_count[row[0]] = row[1]



    # Recent predictions

    cursor.execute(
        """
        SELECT
        filename,
        status,
        probability,
        severity,
        timestamp

        FROM history

        ORDER BY id DESC

        LIMIT 5

        """
    )


    rows = cursor.fetchall()


    recent_predictions=[]


    for row in rows:


        recent_predictions.append(

            {

            "filename":row[0],

            "status":row[1],

            "probability":float(row[2]),

            "severity":row[3],

            "timestamp":row[4]

            }

        )



    conn.close()



    return {


        "total_predictions":

        total_predictions,


        "leakage_detected":

        leakage_detected,


        "normal_cases":

        normal_cases,


        "average_probability":

        round(
            float(avg_probability),
            2
        ),


        "severity_count":

        severity_count,


        "recent_predictions":

        recent_predictions

    }

# ==========================================
# Current Live Alert Status
# ==========================================

@app.get("/alert/status")
def alert_status():

    return latest_alert_status
# ==========================================
# False Alarm Reduction
# ==========================================

LEAK_CONFIRMATION_COUNT = 3

consecutive_leakage_count = 0
