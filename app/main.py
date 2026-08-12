import sys
import os

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "../src"
    )
)


from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware


import pandas as pd
import numpy as np
import pickle
import shutil
import sqlite3


from datetime import datetime


from features.advanced_features import extract_advanced_features

from ml.anomaly_detector import detect_anomaly

from app.sensor import generate_sensor_data




app = FastAPI(
    title="Smart Water Leakage AI",
    version="1.0"
)




# ===============================
# CORS
# ===============================


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)






# ===============================
# Load Model
# ===============================


MODEL_PATH="models/leakage_detector_rf.pkl"


with open(MODEL_PATH,"rb") as f:

    model = pickle.load(f)








# ===============================
# Database
# ===============================


DB_NAME="data/leakage_history.db"



def create_database():


    conn=sqlite3.connect(DB_NAME)

    cursor=conn.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        status TEXT,

        probability REAL,

        severity TEXT,

        timestamp TEXT

        )

        """
    )


    conn.commit()

    conn.close()



create_database()







# ===============================
# Severity
# ===============================


def get_severity(prob):


    if prob < 0.50:

        return "LOW"


    elif prob < 0.80:

        return "MEDIUM"


    else:

        return "HIGH"








# ===============================
# Home
# ===============================


@app.get("/")
def home():

    return {

        "message":
        "Smart Water Leakage AI API Running"

    }









# ===============================
# CSV Prediction
# ===============================


@app.post("/predict")
async def predict(file: UploadFile = File(...)):


    temp_file="temp_sensor.csv"



    with open(temp_file,"wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )



    df=pd.read_csv(temp_file)



    signal=df["Value"].values




    # Anomaly Detection

    anomaly_result = detect_anomaly(signal)





    # Feature Extraction

    features=extract_advanced_features(
        signal
    )



    feature_df=pd.DataFrame(
        [features]
    )




    prediction=model.predict(
        feature_df
    )



    probability=model.predict_proba(
        feature_df
    )[0][1]



    probability=round(
        probability*100,
        2
    )



    severity=get_severity(
        probability/100
    )



    if prediction[0]==1:

        status="Leakage Detected"

    else:

        status="Normal"





    # Save History


    conn=sqlite3.connect(DB_NAME)

    cursor=conn.cursor()


    cursor.execute(

        """

        INSERT INTO history

        (filename,status,probability,severity,timestamp)

        VALUES(?,?,?,?,?)

        """,

        (

        file.filename,

        status,

        probability,

        severity,

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        )

    )


    conn.commit()

    conn.close()



    os.remove(temp_file)





    return {


        "status":status,

        "leakage_probability":probability,

        "severity":severity,

        "signal":signal[:500].tolist(),

        "anomaly":anomaly_result,

        "saved":True

    }









# ===============================
# History
# ===============================


@app.get("/history")
def history():


    conn=sqlite3.connect(DB_NAME)

    cursor=conn.cursor()



    cursor.execute(

        """

        SELECT filename,status,
        probability,severity,timestamp

        FROM history

        ORDER BY id DESC

        """

    )


    rows=cursor.fetchall()


    conn.close()



    result=[]


    for row in rows:


        result.append({

        "filename":row[0],

        "status":row[1],

        "probability":row[2],

        "severity":row[3],

        "timestamp":row[4]

        })



    return result







# ===============================
# Live Sensor
# ===============================


@app.get("/sensor/live")
def live_sensor():


    return generate_sensor_data()







# ===============================
# Live Sensor AI Prediction
# ===============================


@app.post("/sensor/predict")
def sensor_predict(data:dict):


    flow=data["flow_rate"]

    pressure=data["pressure"]

    temperature=data["temperature"]



    signal=np.array([

        flow,

        pressure,

        temperature

    ])



    signal=np.resize(
        signal,
        500
    )



    anomaly_result=detect_anomaly(signal)



    features=extract_advanced_features(
        signal
    )


    feature_df=pd.DataFrame(
        [features]
    )



    prediction=model.predict(
        feature_df
    )


    probability=model.predict_proba(
        feature_df
    )[0][1]



    probability=round(
        probability*100,
        2
    )


    severity=get_severity(
        probability/100
    )



    status="Leakage Detected" if prediction[0]==1 else "Normal"



    return {


        "status":status,

        "leakage_probability":probability,

        "severity":severity,

        "anomaly":anomaly_result,

        "sensor_data":data

    }









# ===============================
# Alert API
# ===============================


@app.get("/alert/status")
def alert_status():


    data=generate_sensor_data()



    signal=np.array([

        data["flow_rate"],

        data["pressure"],

        data["temperature"]

    ])



    signal=np.resize(
        signal,
        500
    )



    anomaly=detect_anomaly(signal)



    features=extract_advanced_features(
        signal
    )


    feature_df=pd.DataFrame(
        [features]
    )



    prediction=model.predict(
        feature_df
    )



    probability=model.predict_proba(
        feature_df
    )[0][1]



    probability=round(
        probability*100,
        2
    )



    return {


        "alert":
        bool(prediction[0]),


        "message":
        "🚨 Water Leakage Detected"
        if prediction[0]==1
        else
        "✅ System Normal",


        "probability":probability,


        "anomaly":anomaly

    }