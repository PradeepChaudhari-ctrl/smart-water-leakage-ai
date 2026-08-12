import pandas as pd
import numpy as np


def extract_features(file_path):
    """
    Extract statistical features from pressure sensor data
    """

    df = pd.read_csv(file_path)

    signal = df["Value"].values

    features = {
        "mean": np.mean(signal),
        "std": np.std(signal),
        "min": np.min(signal),
        "max": np.max(signal),
        "range": np.max(signal) - np.min(signal),
        "rms": np.sqrt(np.mean(signal**2))
    }

    return features


if __name__ == "__main__":

    file = "data/raw/sample/BR_OL_0.18 LPS_P1.csv"

    result = extract_features(file)

    print("Extracted Features:")
    for key, value in result.items():
        print(f"{key}: {value}")