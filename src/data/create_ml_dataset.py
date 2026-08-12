import os
import pandas as pd
from pathlib import Path
from features.extract_features import extract_features


DATA_PATH = "data/raw/sample"
OUTPUT_FILE = "data/processed/features.csv"


def get_label(filename):
    """
    Normal = 0
    Leakage = 1
    """

    if "NL" in filename:
        return 0
    else:
        return 1


def create_dataset():

    rows = []

    for file in os.listdir(DATA_PATH):

        if file.endswith(".csv"):

            file_path = os.path.join(DATA_PATH, file)

            print("Processing:", file)

            features = extract_features(file_path)

            features["filename"] = file
            features["label"] = get_label(file)

            rows.append(features)


    df = pd.DataFrame(rows)

    Path("data/processed").mkdir(
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nDataset created successfully!")
    print(df.head())
    print("\nShape:", df.shape)


if __name__ == "__main__":
    create_dataset()