import os
import pickle
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "dataset",
    "water_leakage_dataset.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "sensor_fusion_rf.pkl"
)


# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv(DATASET_PATH)

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ==========================================
# Features
# ==========================================

FEATURES = [
    "flow_rate",
    "pressure",
    "temperature",
    "usage_duration",
    "vibration"
]

X = df[FEATURES].copy()


# ==========================================
# Target
# ==========================================

y = (
    df["label"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map({
        "normal": 0,
        "leakage": 1
    })
)


if y.isna().any():

    raise ValueError(
        "Dataset contains unknown labels."
    )


# ==========================================
# Train / Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# Random Forest
# ==========================================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)


model.fit(
    X_train,
    y_train
)


# ==========================================
# Evaluation
# ==========================================

predictions = model.predict(X_test)


accuracy = accuracy_score(
    y_test,
    predictions
)

precision = precision_score(
    y_test,
    predictions,
    zero_division=0
)

recall = recall_score(
    y_test,
    predictions,
    zero_division=0
)

f1 = f1_score(
    y_test,
    predictions,
    zero_division=0
)


print("\n================================")
print("MODEL PERFORMANCE")
print("================================")

print(
    f"Accuracy : {accuracy * 100:.2f}%"
)

print(
    f"Precision: {precision * 100:.2f}%"
)

print(
    f"Recall   : {recall * 100:.2f}%"
)

print(
    f"F1 Score : {f1 * 100:.2f}%"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        target_names=[
            "Normal",
            "Leakage"
        ],
        zero_division=0
    )
)


# ==========================================
# Feature Importance
# ==========================================

print("\nFeature Importance:")

for name, importance in zip(
    FEATURES,
    model.feature_importances_
):

    print(
        f"{name:18} : "
        f"{importance:.4f}"
    )


# ==========================================
# Save Model
# ==========================================

os.makedirs(
    os.path.dirname(MODEL_PATH),
    exist_ok=True
)


with open(
    MODEL_PATH,
    "wb"
) as file:

    pickle.dump(
        model,
        file
    )


print(
    "\nModel saved:"
)

print(
    MODEL_PATH
)