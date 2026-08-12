import os
import zipfile
import pandas as pd
from pathlib import Path

from features.advanced_features import extract_advanced_features


ZIP_FILE = "data/raw/Dynamic Pressure Sensor.zip"

EXTRACT_PATH = "data/raw/sensor_data"

OUTPUT_FILE = "data/processed/full_features.csv"


def get_label(filename):
    """
    No-leak = 0
    Other conditions = 1
    """

    if "NL" in filename:
        return 0
    else:
        return 1



def extract_zip():

    if not os.path.exists(EXTRACT_PATH):

        print("Extracting dataset...")

        with zipfile.ZipFile(ZIP_FILE, "r") as zip_ref:
            zip_ref.extractall(EXTRACT_PATH)

        print("Extraction complete")

    else:
        print("Dataset already extracted")



def create_dataset():

    rows = []

    for root, dirs, files in os.walk(EXTRACT_PATH):

        for file in files:

            if file.endswith(".csv"):

                file_path = os.path.join(root, file)

                try:

                    print("Processing:", file)

                    # Read sensor CSV
                    df = pd.read_csv(file_path)

                    # Extract pressure signal
                    signal = df["Value"].values


                    # Advanced feature extraction
                    features = extract_advanced_features(signal)


                    # Add metadata
                    features["filename"] = file

                    features["label"] = get_label(file)


                    rows.append(features)


                except Exception as e:

                    print("Skipped:", file, e)



    df = pd.DataFrame(rows)


    Path("data/processed").mkdir(
        exist_ok=True
    )


    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print("\nDataset Created Successfully")

    print("Shape:", df.shape)

    print(df.head())



if __name__ == "__main__":

    extract_zip()

    create_dataset()