import pandas as pd
import joblib

from features.extract_features import extract_features


MODEL_PATH = "models/leakage_detector.pkl"


def predict(file_path):

    # Load trained model
    model = joblib.load(MODEL_PATH)


    # Extract sensor features
    features = extract_features(file_path)


    X = pd.DataFrame(
        [features]
    )


    # Keep same order as training
    X = X[
        [
            "mean",
            "std",
            "min",
            "max",
            "range",
            "rms"
        ]
    ]


    # Prediction
    prediction = model.predict(X)[0]


    probability = model.predict_proba(X)[0]


    print("\nPrediction Result")

    if prediction == 1:
        print("Status: ⚠️ Leakage Detected")
    else:
        print("Status: ✅ Normal")


    print(
        "Leakage Probability:",
        round(probability[1]*100, 2),
        "%"
    )



if __name__ == "__main__":

    test_file = (
        "data/raw/sample/"
        "BR_OL_0.18 LPS_P1.csv"
    )

    predict(test_file)