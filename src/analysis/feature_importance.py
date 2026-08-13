import pandas as pd

from sklearn.ensemble import RandomForestClassifier


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
# Feature Importance
# ==========================================

def analyze_feature_importance(X, y):

    print("\n===================================")
    print("💧 Smart Water Leakage AI")
    print("🧠 Feature Importance")
    print("===================================\n")


    model = RandomForestClassifier(

        n_estimators=200,

        random_state=42,

        class_weight="balanced"

    )


    model.fit(
        X,
        y
    )


    importance = pd.DataFrame({

        "feature": X.columns,

        "importance": model.feature_importances_

    })


    importance = importance.sort_values(

        by="importance",

        ascending=False

    )


    print("Feature Importance:\n")


    for _, row in importance.iterrows():

        print(
            f"{row['feature']:15} : "
            f"{row['importance']:.4f}"
        )


    return importance


# ==========================================
# Main
# ==========================================

def main():

    X, y = load_dataset()

    importance = analyze_feature_importance(
        X,
        y
    )


    # Save results

    importance.to_csv(

        "data/processed/feature_importance.csv",

        index=False

    )


    print(
        "\n✅ Saved:"
        " data/processed/feature_importance.csv"
    )


# ==========================================
# Run
# ==========================================

if __name__ == "__main__":

    main()