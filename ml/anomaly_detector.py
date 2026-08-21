import numpy as np


def detect_anomaly(signal):

    signal = np.asarray(signal, dtype=float)

    # Empty signal protection
    if signal.size == 0:

        return {
            "status": "Unavailable",
            "anomaly_score": 0.0,
            "anomaly_count": 0
        }

    mean = float(np.mean(signal))
    std = float(np.std(signal))

    # Constant signal protection
    if std == 0:

        return {
            "status": "Normal",
            "anomaly_score": 0.0,
            "anomaly_count": 0
        }

    z_scores = np.abs(
        (signal - mean) / std
    )

    anomalies = signal[
        z_scores > 2.5
    ]

    anomaly_count = int(
        len(anomalies)
    )

    anomaly_score = (
        anomaly_count / len(signal)
    ) * 100

    if anomaly_score > 20:

        status = "Abnormal"

    else:

        status = "Normal"

    return {

        "status": status,

        "anomaly_score":
            round(
                float(anomaly_score),
                2
            ),

        "anomaly_count":
            anomaly_count

    }