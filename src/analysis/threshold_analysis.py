import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# ==========================================
# Configuration
# ==========================================

DATASET = "data/processed/full_features.csv"


# Thresholds we want to test
THRESHOLDS = [
    0.30,
    0.35,
    0.40,
    0.45,
    0.50,
    0.55,
    0.60,
    0.65,
    0.70
]


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
# Main
# ==========================================

def main():

    print("\n===================================")
    print("💧 Smart Water Leakage AI")
    print("🎯 Threshold Optimization")
    print("===================================\n")


    X, y = load_dataset()


    print("Dataset Shape:", X.shape)


    # ======================================
    # Cross Validation
    # ======================================

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )


    # ======================================
    # Random Forest
    # ======================================

    model = RandomForestClassifier(

        n_estimators=200,

        random_state=42,

        class_weight="balanced"

    )


    # ======================================
    # Get Cross-Validated Probabilities
    # ======================================

    probabilities = cross_val_predict(

        model,

        X,

        y,

        cv=cv,

        method="predict_proba"

    )[:, 1]


    results = []


    # ======================================
    # Test Thresholds
    # ======================================

    for threshold in THRESHOLDS:

        prediction = (
            probabilities >= threshold
        ).astype(int)


        precision = precision_score(

            y,

            prediction,

            zero_division=0

        )


        recall = recall_score(

            y,

            prediction,

            zero_division=0

        )


        f1 = f1_score(

            y,

            prediction,

            zero_division=0

        )


        cm = confusion_matrix(

            y,

            prediction

        )


        tn, fp, fn, tp = cm.ravel()


        results.append({

            "threshold": threshold,

            "precision": precision,

            "recall": recall,

            "f1": f1,

            "true_negative": tn,

            "false_positive": fp,

            "false_negative": fn,

            "true_positive": tp

        })


    result_df = pd.DataFrame(
        results
    )


    # ======================================
    # Display Results
    # ======================================

    print("\n===================================")
    print("📊 Threshold Results")
    print("===================================\n")


    print(

        result_df.to_string(

            index=False,

            float_format=lambda x: f"{x:.4f}"

        )

    )


    # ======================================
    # Best F1 Threshold
    # ======================================

    best_f1 = result_df.loc[
        result_df["f1"].idxmax()
    ]


    print("\n===================================")
    print("🏆 BEST F1 THRESHOLD")
    print("===================================\n")


    print(
        f"Threshold : "
        f"{best_f1['threshold']:.2f}"
    )

    print(
        f"Precision : "
        f"{best_f1['precision']:.4f}"
    )

    print(
        f"Recall    : "
        f"{best_f1['recall']:.4f}"
    )

    print(
        f"F1 Score  : "
        f"{best_f1['f1']:.4f}"
    )

    print(
        f"False Negatives: "
        f"{int(best_f1['false_negative'])}"
    )


    # ======================================
    # Best Recall Threshold
    # ======================================

    best_recall = result_df.loc[
        result_df["recall"].idxmax()
    ]


    print("\n===================================")
    print("🚨 BEST RECALL THRESHOLD")
    print("===================================\n")


    print(
        f"Threshold : "
        f"{best_recall['threshold']:.2f}"
    )

    print(
        f"Precision : "
        f"{best_recall['precision']:.4f}"
    )

    print(
        f"Recall    : "
        f"{best_recall['recall']:.4f}"
    )

    print(
        f"F1 Score  : "
        f"{best_recall['f1']:.4f}"
    )

    print(
        f"False Negatives: "
        f"{int(best_recall['false_negative'])}"
    )


    # ======================================
    # Save Results
    # ======================================

    output_file = (
        "data/processed/threshold_results.csv"
    )


    result_df.to_csv(

        output_file,

        index=False

    )


    print(
        "\n✅ Results saved:"
    )

    print(output_file)


    print("\n===================================")
    print("✅ Threshold Analysis Completed")
    print("===================================\n")


# ==========================================
# Run
# ==========================================

if __name__ == "__main__":

    main()