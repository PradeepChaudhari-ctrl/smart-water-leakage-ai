import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)


DATASET = "data/processed/full_features.csv"


def load_dataset():

    df = pd.read_csv(DATASET)

    print("Dataset Shape:", df.shape)

    print("\nLabel Distribution:")
    print(df["label"].value_counts())


    # Remove non-feature columns
    X = df.drop(
        columns=["filename", "label"]
    )

    y = df["label"]


    return X, y



def evaluate_model(name, model, X_test, y_test):

    prediction = model.predict(X_test)

    probability = model.predict_proba(X_test)[:,1]


    print("\n======================")
    print(name)
    print("======================")


    print("Accuracy:")
    print(accuracy_score(y_test, prediction))


    print("\nROC-AUC:")
    print(roc_auc_score(y_test, probability))


    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            prediction,
            zero_division=0
        )
    )


    print("Confusion Matrix:")
    print(
        confusion_matrix(
            y_test,
            prediction
        )
    )



def main():

    X, y = load_dataset()


    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )


    # Random Forest
    rf_model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )


    rf_model.fit(
        X_train,
        y_train
    )


    evaluate_model(
        "Random Forest",
        rf_model,
        X_test,
        y_test
    )


    # XGBoost
    xgb_model = XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=4,
        random_state=42
    )


    xgb_model.fit(
        X_train,
        y_train
    )


    evaluate_model(
        "XGBoost",
        xgb_model,
        X_test,
        y_test
    )



if __name__ == "__main__":
    main()