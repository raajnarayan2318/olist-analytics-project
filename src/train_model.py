from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib  # pip install joblib if needed

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "ml_delivery_dataset.parquet"
MODEL_PATH = BASE_DIR / "data" / "processed" / "delivery_risk_model.joblib"

def main():
    df = pd.read_parquet(DATA_PATH)

    # Define label
    df["is_late"] = df["is_late"].astype(int)

    # Drop high-cardinality identifiers
    df = df.drop(columns=["order_id", "customer_unique_id"])

    # Separate features and target
    X = df.drop(columns=["is_late", "delivery_days"])  # avoid leakage
    y = df["is_late"]

    # Identify numeric and categorical columns
    numeric_features = ["price", "freight_value", "estimated_delivery_days",
                        "purchase_dow", "purchase_month", "purchase_year"]
    categorical_features = ["customer_state", "seller_state", "product_category_name"]

    numeric_transformer = Pipeline(steps=[
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=-1
    )

    clf = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)[:, 1]

    print(classification_report(y_test, y_pred))
    print("ROC AUC:", roc_auc_score(y_test, y_proba))

    # Save model
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    main()
