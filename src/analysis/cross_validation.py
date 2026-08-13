import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate


# ==========================================
# Configuration
# ==========================================

DATASET = "data/processed/full_features.csv"


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
    print("🔬 5-Fold Cross Validation")
    print("===================================\n")


    X, y = load_dataset()


    print("Dataset Shape:", X.shape)

    print("\nLabel Distribution:")
    print(y.value_counts())


    # ======================================
    # Random Forest
    # ======================================

    model = RandomForestClassifier(

        n_estimators=200,

        random_state=42,

        class_weight="balanced"

    )


    # ======================================
    # Stratified K-Fold
    # ======================================

    cv = StratifiedKFold(

        n_splits=5,

        shuffle=True,

        random_state=42

    )


    # ======================================
    # Evaluation Metrics
    # ======================================

    scoring = {

        "accuracy": "accuracy",

        "precision": "precision",

        "recall": "recall",

        "f1": "f1",

        "roc_auc": "roc_auc"

    }


    results = cross_validate(

        model,

        X,

        y,

        cv=cv,

        scoring=scoring

    )


    # ======================================
    # Results
    # ======================================

    print("\n===================================")
    print("📊 Cross Validation Results")
    print("===================================\n")


    print(
        f"Accuracy : "
        f"{results['test_accuracy'].mean():.4f}"
    )


    print(
        f"Precision: "
        f"{results['test_precision'].mean():.4f}"
    )


    print(
        f"Recall   : "
        f"{results['test_recall'].mean():.4f}"
    )


    print(
        f"F1 Score : "
        f"{results['test_f1'].mean():.4f}"
    )


    print(
        f"ROC-AUC  : "
        f"{results['test_roc_auc'].mean():.4f}"
    )


    # ======================================
    # Fold-by-Fold Results
    # ======================================

    print("\n===================================")
    print("📈 Fold Results")
    print("===================================\n")


    for i in range(5):

        print(
            f"Fold {i + 1}: "
            f"Accuracy = "
            f"{results['test_accuracy'][i]:.4f}, "
            f"F1 = "
            f"{results['test_f1'][i]:.4f}, "
            f"ROC-AUC = "
            f"{results['test_roc_auc'][i]:.4f}"
        )


    print("\n===================================")
    print("✅ Cross Validation Completed")
    print("===================================\n")


# ==========================================
# Run
# ==========================================

if __name__ == "__main__":

    main()