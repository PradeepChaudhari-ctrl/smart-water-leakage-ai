import pandas as pd
from pathlib import Path


# ==========================================
# Configuration
# ==========================================

DATASET = "data/processed/full_features.csv"


# ==========================================
# Load Dataset
# ==========================================

def load_dataset():

    print("\n===================================")
    print("💧 Smart Water Leakage AI")
    print("📊 Dataset Analysis")
    print("===================================\n")

    df = pd.read_csv(DATASET)

    print("Total Samples:", len(df))

    print("\nDataset Shape:")
    print(df.shape)

    return df


# ==========================================
# Label Analysis
# ==========================================

def analyze_labels(df):

    print("\n===================================")
    print("🏷️ Label Distribution")
    print("===================================")

    counts = df["label"].value_counts()

    normal = counts.get(0, 0)
    leakage = counts.get(1, 0)

    print("Normal Samples :", normal)
    print("Leakage Samples:", leakage)

    total = len(df)

    if total > 0:

        print(
            f"\nNormal Percentage : {(normal / total) * 100:.2f}%"
        )

        print(
            f"Leakage Percentage: {(leakage / total) * 100:.2f}%"
        )


# ==========================================
# Leakage Type Analysis
# ==========================================

def analyze_leakage_types(df):

    print("\n===================================")
    print("💧 Leakage Type Distribution")
    print("===================================")

    filenames = df["filename"].astype(str)

    leakage_types = {

        "Longitudinal Crack": filenames.str.contains(
            "_LC_",
            regex=False
        ),

        "Orifice Leak": filenames.str.contains(
            "_OL_",
            regex=False
        ),

        "Circumferential Crack": filenames.str.contains(
            "_CC_",
            regex=False
        ),

        "Gasket Leak": filenames.str.contains(
            "_GL_",
            regex=False
        ),

        "No Leak": filenames.str.contains(
            "_NL_",
            regex=False
        )

    }

    for name, mask in leakage_types.items():

        print(
            f"{name:25} : {mask.sum()}"
        )


# ==========================================
# Pipeline Type
# ==========================================

def analyze_pipeline(df):

    print("\n===================================")
    print("🔧 Pipeline Configuration")
    print("===================================")

    filenames = df["filename"].astype(str)

    branched = filenames.str.startswith("BR_").sum()
    looped = filenames.str.startswith("LO_").sum()

    print("Branched Pipeline:", branched)
    print("Looped Pipeline  :", looped)


# ==========================================
# Flow / Test Condition
# ==========================================

def analyze_conditions(df):

    print("\n===================================")
    print("🌊 Test Conditions")
    print("===================================")

    filenames = df["filename"].astype(str)

    conditions = {

        "0.18 LPS": filenames.str.contains(
            "0.18 LPS",
            regex=False
        ),

        "0.47 LPS": filenames.str.contains(
            "0.47 LPS",
            regex=False
        ),

        "ND": filenames.str.contains(
            "_ND_",
            regex=False
        ),

        "Transient": filenames.str.contains(
            "Transient",
            regex=False
        )

    }

    for name, mask in conditions.items():

        print(
            f"{name:15} : {mask.sum()}"
        )


# ==========================================
# Feature Analysis
# ==========================================

def analyze_features(df):

    print("\n===================================")
    print("🧠 Feature Information")
    print("===================================")

    feature_columns = [

        "mean",
        "std",
        "min",
        "max",
        "range",
        "rms",
        "energy",
        "variance",
        "skewness",
        "kurtosis",
        "mean_change",
        "max_change"

    ]

    print("\nFeatures Used:")

    for feature in feature_columns:

        if feature in df.columns:

            print("✔", feature)

        else:

            print("❌ Missing:", feature)


# ==========================================
# Main
# ==========================================

def main():

    if not Path(DATASET).exists():

        print(
            f"\n❌ Dataset not found: {DATASET}"
        )

        return


    df = load_dataset()

    analyze_labels(df)

    analyze_leakage_types(df)

    analyze_pipeline(df)

    analyze_conditions(df)

    analyze_features(df)


    print("\n===================================")
    print("✅ Dataset Analysis Completed")
    print("===================================\n")


# ==========================================
# Run
# ==========================================

if __name__ == "__main__":

    main()