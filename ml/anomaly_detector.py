import numpy as np


def detect_anomaly(signal):


    signal = np.array(signal)



    mean = np.mean(signal)


    std = np.std(signal)



    anomalies = []



    for value in signal:


        z_score = abs(
            (value-mean)/std
        )


        if z_score > 2.5:

            anomalies.append(value)



    anomaly_score = (
        len(anomalies)
        /
        len(signal)
    ) * 100



    if anomaly_score > 20:


        status = "Abnormal"


    else:


        status = "Normal"



    return {

        "status":status,

        "anomaly_score":
        round(anomaly_score,2),

        "anomaly_count":
        len(anomalies)

    }