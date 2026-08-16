import joblib
import numpy as np


# Load trained AI model

model = joblib.load(
    "../models/leakage_model.pkl"
)



def predict_leakage(
    flow_rate,
    pressure,
    temperature,
    usage_duration,
    vibration
):


    data = np.array([

        [
            flow_rate,
            pressure,
            temperature,
            usage_duration,
            vibration
        ]

    ])



    prediction = model.predict(data)[0]



    probability = model.predict_proba(data)[0]



    if prediction == 0:

        status = "Leakage Detected"

    else:

        status = "Normal"



    return {

        "status": status,

        "leakage_probability":
        round(
            max(probability)*100,
            2
        )

    }