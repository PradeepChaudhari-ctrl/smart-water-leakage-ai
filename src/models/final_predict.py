import pandas as pd
import pickle
import numpy as np

from features.advanced_features import extract_advanced_features


MODEL_PATH = "models/leakage_detector_rf.pkl"


# Test sensor file
INPUT_FILE = "data/raw/sample/BR_OL_0.18 LPS_P1.csv"


def get_severity(probability):

    if probability < 0.50:
        return "LOW"

    elif probability < 0.80:
        return "MEDIUM"

    else:
        return "HIGH"



def main():

    print("Loading model...")


    # Load trained model
    with open(
        MODEL_PATH,
        "rb"
    ) as file:

        model = pickle.load(file)



    print("Reading sensor data...")


    df = pd.read_csv(INPUT_FILE)


    # CSV me Value column hai
    signal = df["Value"].values



    # Extract features

    features = extract_advanced_features(
        signal
    )


    # Convert dictionary to dataframe

    feature_df = pd.DataFrame(
        [features]
    )


    print("\nExtracted Features:")
    print(feature_df)



    # Prediction

    prediction = model.predict(
        feature_df
    )


    probability = model.predict_proba(
        feature_df
    )[0][1]



    severity = get_severity(
        probability
    )


    print("\n========================")
    print("Smart Water Leakage AI")
    print("========================")


    if prediction[0] == 1:
        print("Status: ⚠️ Leakage Detected")

    else:
        print("Status: ✅ Normal")



    print(
        f"Leakage Probability: {probability*100:.2f}%"
    )


    print(
        "Severity:",
        severity
    )



if __name__ == "__main__":
    main()