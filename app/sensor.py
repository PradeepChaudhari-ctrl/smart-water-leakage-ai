import random
from datetime import datetime


def generate_sensor_data():

    # ==========================================
    # Random Pipeline Condition
    # ==========================================

    condition = random.choice(
        [
            "normal",
            "normal",
            "normal",
            "warning",
            "leakage"
        ]
    )

    # ==========================================
    # NORMAL PIPELINE
    # ==========================================

    if condition == "normal":

        flow_rate = round(
            random.uniform(30, 55),
            2
        )

        pressure = round(
            random.uniform(280, 350),
            2
        )

        temperature = round(
            random.uniform(20, 27),
            2
        )

        usage_duration = round(
            random.uniform(20, 70),
            2
        )

        vibration = round(
            random.uniform(0.10, 0.30),
            2
        )

        status = "Normal"

    # ==========================================
    # WARNING CONDITION
    # ==========================================

    elif condition == "warning":

        flow_rate = round(
            random.uniform(55, 70),
            2
        )

        pressure = round(
            random.uniform(180, 280),
            2
        )

        temperature = round(
            random.uniform(25, 32),
            2
        )

        usage_duration = round(
            random.uniform(60, 90),
            2
        )

        vibration = round(
            random.uniform(0.30, 0.55),
            2
        )

        status = "Warning"

    # ==========================================
    # LEAKAGE CONDITION
    # ==========================================

    else:

        flow_rate = round(
            random.uniform(70, 100),
            2
        )

        pressure = round(
            random.uniform(80, 180),
            2
        )

        temperature = round(
            random.uniform(28, 35),
            2
        )

        usage_duration = round(
            random.uniform(80, 120),
            2
        )

        vibration = round(
            random.uniform(0.55, 1.00),
            2
        )

        status = "Leakage"

    # ==========================================
    # Return Sensor Data
    # ==========================================

    return {

        "timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "flow_rate":
            flow_rate,

        "pressure":
            pressure,

        "temperature":
            temperature,

        "usage_duration":
            usage_duration,

        "vibration":
            vibration,

        "status":
            status
    }