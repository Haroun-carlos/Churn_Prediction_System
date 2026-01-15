import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
import os

def load_and_preprocess_data(filepath):
    df = pd.read_csv(filepath)

    # =========================
    # Explicit data cleaning
    # =========================
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(subset=["TotalCharges"], inplace=True)

    # SeniorCitizen is categorical, not numeric
    df["SeniorCitizen"] = df["SeniorCitizen"].astype(str)

    # Target encoding
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    # =========================
    # Feature / target split
    # =========================
    X = df.drop(columns=["customerID", "Churn"])
    y = df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    numerical_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()

    # =========================
    # Preprocessing pipelines
    # =========================
    numerical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numerical_pipeline, numerical_cols),
            ("cat", categorical_pipeline, categorical_cols)
        ]
    )

    return X_train, X_test, y_train, y_test, preprocessor


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, preprocessor = load_and_preprocess_data(
        "data/telco_churn.csv"
    )

    X_train_p = preprocessor.fit_transform(X_train)
    X_test_p = preprocessor.transform(X_test)

    os.makedirs("models", exist_ok=True)

    joblib.dump(preprocessor, "models/preprocessor.joblib")
    np.save("data/X_train_processed.npy", X_train_p)
    np.save("data/X_test_processed.npy", X_test_p)
    np.save("data/y_train.npy", y_train)
    np.save("data/y_test.npy", y_test)

    print("✅ Preprocessing completed.")
