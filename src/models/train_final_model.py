import pandas as pd
import pickle
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier


DATASET = "data/processed/full_features.csv"

MODEL_PATH = "models/leakage_detector_rf.pkl"


def main():

    print("Loading dataset...")

    df = pd.read_csv(DATASET)

    print("Dataset Shape:", df.shape)


    # Features and label

    X = df.drop(
        columns=[
            "filename",
            "label"
        ]
    )

    y = df["label"]


    print("\nTraining Random Forest...")


    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )


    model.fit(
        X,
        y
    )


    # Create models folder

    Path("models").mkdir(
        exist_ok=True
    )


    # Save model

    with open(
        MODEL_PATH,
        "wb"
    ) as file:

        pickle.dump(
            model,
            file
        )


    print("\nFinal Model Saved!")
    print(MODEL_PATH)


    print("\nFeature Used:")
    print(list(X.columns))


if __name__ == "__main__":
    main()