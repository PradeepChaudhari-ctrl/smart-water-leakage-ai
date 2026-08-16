import pandas as pd
import random


data = []


for i in range(2000):

    # Normal condition
    if random.random() < 0.7:

        flow_rate = random.uniform(30,60)
        pressure = random.uniform(280,350)
        temperature = random.uniform(20,30)
        usage_duration = random.randint(30,120)
        vibration = random.uniform(0.1,0.3)
        label = "Normal"


    # Leakage condition
    else:

        flow_rate = random.uniform(70,120)
        pressure = random.uniform(100,220)
        temperature = random.uniform(25,35)
        usage_duration = random.randint(40,150)
        vibration = random.uniform(0.5,1.0)
        label = "Leakage"



    data.append({

        "flow_rate": round(flow_rate,2),

        "pressure": round(pressure,2),

        "temperature": round(temperature,2),

        "usage_duration": usage_duration,

        "vibration": round(vibration,2),

        "label": label

    })



df = pd.DataFrame(data)


df.to_csv(
    "dataset/water_leakage_dataset.csv",
    index=False
)


print("Dataset Generated Successfully")
print(df.head())