import random
from datetime import datetime



def generate_sensor_data():


    flow_rate = round(
        random.uniform(2,8),
        2
    )


    pressure = round(
        random.uniform(1800,2600),
        2
    )


    temperature = round(
        random.uniform(22,30),
        2
    )



    if pressure < 2000 or flow_rate > 7:

        status = "Warning"

    else:

        status = "Normal"



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