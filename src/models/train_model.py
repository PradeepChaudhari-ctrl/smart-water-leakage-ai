import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

import joblib
from pathlib import Path


DATASET = "data/processed/full_features.csv"

MODEL_PATH = "models/leakage_detector.pkl"


def train():

    # Load dataset
    df = pd.read_csv(DATASET)

    print("Dataset shape:", df.shape)
    print(df["label"].value_counts())


    # Features
    X = df[
        [
            "mean",
            "std",
            "min",
            "max",
            "range",
            "rms"
        ]
    ]

    # Target
    y = df["label"]


    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )


    # Model
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    )


    # Training
    model.fit(
        X_train,
        y_train
    )


    # Prediction
    y_pred = model.predict(X_test)


    print("\nAccuracy:")
    print(
        accuracy_score(
            y_test,
            y_pred
        )
    )


    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred
        )
    )


    print("\nConfusion Matrix:")
    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )


    # Save model
    Path("models").mkdir(
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_PATH
    )

    print("\nModel saved:", MODEL_PATH)



if __name__ == "__main__":
    train()