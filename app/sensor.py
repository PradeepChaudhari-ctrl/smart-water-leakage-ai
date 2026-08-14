import random
from datetime import datetime


def generate_sensor_data():

    # Random situation generate
    condition = random.choice(
        [
            "normal",
            "normal",
            "normal",
            "warning",
            "leakage"
        ]
    )


    # ==========================
    # NORMAL PIPELINE
    # ==========================

    if condition == "normal":

        flow_rate = round(
            random.uniform(3,6),
            2
        )

        pressure = round(
            random.uniform(2200,2600),
            2
        )

        temperature = round(
            random.uniform(22,27),
            2
        )

        status = "Normal"



    # ==========================
    # WARNING CONDITION
    # ==========================

    elif condition == "warning":

        flow_rate = round(
            random.uniform(6,7.5),
            2
        )

        pressure = round(
            random.uniform(1900,2200),
            2
        )

        temperature = round(
            random.uniform(27,30),
            2
        )

        status = "Warning"



    # ==========================
    # LEAKAGE CONDITION
    # ==========================

    else:

        flow_rate = round(
            random.uniform(8,12),
            2
        )

        pressure = round(
            random.uniform(1000,1700),
            2
        )

        temperature = round(
            random.uniform(30,35),
            2
        )

        status = "Leakage"



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


        "status":
        status

    }