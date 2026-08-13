import pandas as pd

from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


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
    print("🤖 Model Comparison")
    print("🔬 5-Fold Cross Validation")
    print("===================================\n")


    X, y = load_dataset()


    print("Dataset Shape:", X.shape)

    print("\nLabel Distribution:")
    print(y.value_counts())


    # ======================================
    # Cross Validation
    # ======================================

    cv = StratifiedKFold(

        n_splits=5,

        shuffle=True,

        random_state=42

    )


    # ======================================
    # Models
    # ======================================

    models = {

        "Random Forest": RandomForestClassifier(

            n_estimators=200,

            random_state=42,

            class_weight="balanced"

        ),


        "Logistic Regression": LogisticRegression(

            max_iter=2000,

            class_weight="balanced",

            random_state=42

        ),


        "SVM": SVC(

            probability=True,

            class_weight="balanced",

            random_state=42

        )

    }


    # ======================================
    # Metrics
    # ======================================

    scoring = {

        "accuracy": "accuracy",

        "precision": "precision",

        "recall": "recall",

        "f1": "f1",

        "roc_auc": "roc_auc"

    }


    results = []


    # ======================================
    # Evaluate Models
    # ======================================

    for name, model in models.items():

        print("\n-----------------------------------")
        print(f"🔎 Evaluating: {name}")
        print("-----------------------------------")


        scores = cross_validate(

            model,

            X,

            y,

            cv=cv,

            scoring=scoring

        )


        accuracy = scores[
            "test_accuracy"
        ].mean()


        precision = scores[
            "test_precision"
        ].mean()


        recall = scores[
            "test_recall"
        ].mean()


        f1 = scores[
            "test_f1"
        ].mean()


        roc_auc = scores[
            "test_roc_auc"
        ].mean()


        results.append({

            "Model": name,

            "Accuracy": accuracy,

            "Precision": precision,

            "Recall": recall,

            "F1": f1,

            "ROC-AUC": roc_auc

        })


        print(
            f"Accuracy : {accuracy:.4f}"
        )

        print(
            f"Precision: {precision:.4f}"
        )

        print(
            f"Recall   : {recall:.4f}"
        )

        print(
            f"F1 Score : {f1:.4f}"
        )

        print(
            f"ROC-AUC  : {roc_auc:.4f}"
        )


    # ======================================
    # Comparison Table
    # ======================================

    result_df = pd.DataFrame(results)


    print("\n===================================")
    print("📊 FINAL MODEL COMPARISON")
    print("===================================\n")


    print(
        result_df.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )


    # ======================================
    # Best Model
    # ======================================

    best_model = result_df.loc[
        result_df["ROC-AUC"].idxmax()
    ]


    print("\n===================================")
    print("🏆 BEST MODEL")
    print("===================================\n")


    print(
        "Model:",
        best_model["Model"]
    )


    print(
        f"ROC-AUC: "
        f"{best_model['ROC-AUC']:.4f}"
    )


    print(
        f"F1 Score: "
        f"{best_model['F1']:.4f}"
    )


    # ======================================
    # Save Results
    # ======================================

    output_file = (
        "data/processed/model_comparison.csv"
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
    print("✅ Model Comparison Completed")
    print("===================================\n")


# ==========================================
# Run
# ==========================================

if __name__ == "__main__":

    main()