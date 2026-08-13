import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve,
    roc_auc_score
)

from pathlib import Path


# ==========================================
# Configuration
# ==========================================

DATASET = "data/processed/full_features.csv"

OUTPUT_DIR = Path("data/processed")


# ==========================================
# Load Dataset
# ==========================================

def load_dataset():

    df = pd.read_csv(DATASET)

    X = df.drop(
        columns=[
            "filename",
            "label"
        ]
    )

    y = df["label"]

    return X, y


# ==========================================
# Train Model
# ==========================================

def train_model(X_train, y_train):

    model = RandomForestClassifier(

        n_estimators=200,

        random_state=42,

        class_weight="balanced"

    )

    model.fit(
        X_train,
        y_train
    )

    return model


# ==========================================
# Confusion Matrix
# ==========================================

def create_confusion_matrix(
    model,
    X_test,
    y_test
):

    prediction = model.predict(
        X_test
    )

    cm = confusion_matrix(
        y_test,
        prediction
    )


    print("\n===================================")
    print("📊 Confusion Matrix")
    print("===================================\n")

    print(cm)


    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=[
            "Normal",
            "Leakage"
        ]
    )


    display.plot()

    plt.title(
        "Smart Water Leakage AI - Confusion Matrix"
    )

    plt.tight_layout()


    output = (
        OUTPUT_DIR /
        "confusion_matrix.png"
    )


    plt.savefig(
        output,
        dpi=150
    )

    plt.close()


    print(
        "\n✅ Confusion Matrix saved:"
    )

    print(output)


# ==========================================
# ROC Curve
# ==========================================

def create_roc_curve(
    model,
    X_test,
    y_test
):

    probability = model.predict_proba(
        X_test
    )[:, 1]


    fpr, tpr, thresholds = roc_curve(
        y_test,
        probability
    )


    auc_score = roc_auc_score(
        y_test,
        probability
    )


    print("\n===================================")
    print("📈 ROC-AUC")
    print("===================================")

    print(
        f"\nROC-AUC Score: {auc_score:.4f}"
    )


    plt.figure()


    plt.plot(
        fpr,
        tpr,
        label=f"Random Forest (AUC = {auc_score:.4f})"
    )


    plt.plot(
        [0, 1],
        [0, 1],
        linestyle="--",
        label="Random Guess"
    )


    plt.xlabel(
        "False Positive Rate"
    )

    plt.ylabel(
        "True Positive Rate"
    )


    plt.title(
        "Smart Water Leakage AI - ROC Curve"
    )


    plt.legend()


    plt.tight_layout()


    output = (
        OUTPUT_DIR /
        "roc_curve.png"
    )


    plt.savefig(
        output,
        dpi=150
    )

    plt.close()


    print(
        "\n✅ ROC Curve saved:"
    )

    print(output)


# ==========================================
# Main
# ==========================================

def main():

    print("\n===================================")
    print("💧 Smart Water Leakage AI")
    print("📊 Model Visualization")
    print("===================================\n")


    OUTPUT_DIR.mkdir(
        exist_ok=True
    )


    X, y = load_dataset()


    # Same split configuration as
    # our previous model evaluation

    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,

        test_size=0.25,

        random_state=42,

        stratify=y

    )


    print(
        "Training Samples:",
        len(X_train)
    )

    print(
        "Testing Samples:",
        len(X_test)
    )


    model = train_model(
        X_train,
        y_train
    )


    create_confusion_matrix(
        model,
        X_test,
        y_test
    )


    create_roc_curve(
        model,
        X_test,
        y_test
    )


    print("\n===================================")
    print("✅ Visualization Completed")
    print("===================================\n")


# ==========================================
# Run
# ==========================================

if __name__ == "__main__":

    main()