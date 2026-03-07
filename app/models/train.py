import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, accuracy_score

from app.utils.preprocessing import load_data, prepare_features


def main():
    """Train crop yield prediction and crop extinction risk models"""

    print("Loading dataset...")

    data_path = "C:/Users/hr479/Downloads/Crop_Tool/data/processed/advanced_crop_yield_dataset_12000_rows.csv"
    df = load_data(data_path)

    if df is None or df.empty:
        print("❌ Dataset not loaded.")
        return

    print("Dataset loaded successfully.")
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}")

    # Prepare features for yield prediction
    print("\nPreparing features...")
    X, y_yield = prepare_features(df)

    # Risk target
    if "crop_extinction_risk" not in df.columns:
        print("❌ 'crop_extinction_risk' column not found in dataset.")
        return

    y_risk = df["crop_extinction_risk"]

    # Split dataset
    print("\nSplitting dataset...")
    X_train, X_test, y_train_yield, y_test_yield = train_test_split(
        X, y_yield, test_size=0.2, random_state=42
    )

    y_train_risk = y_risk.loc[X_train.index]
    y_test_risk = y_risk.loc[X_test.index]

    # ===============================
    # Train Yield Prediction Model
    # ===============================

    print("\nTraining Yield Prediction Model...")

    yield_model = RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        random_state=42
    )

    yield_model.fit(X_train, y_train_yield)

    # Evaluate
    yield_train_pred = yield_model.predict(X_train)
    yield_test_pred = yield_model.predict(X_test)

    train_r2 = r2_score(y_train_yield, yield_train_pred)
    test_r2 = r2_score(y_test_yield, yield_test_pred)

    print(f"Yield Model Training R²: {train_r2:.3f}")
    print(f"Yield Model Testing R²: {test_r2:.3f}")

    # ===============================
    # Train Crop Risk Model
    # ===============================

    print("\nTraining Crop Extinction Risk Model...")

    risk_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42
    )

    risk_model.fit(X_train, y_train_risk)

    # Evaluate
    risk_train_pred = risk_model.predict(X_train)
    risk_test_pred = risk_model.predict(X_test)

    train_acc = accuracy_score(y_train_risk, risk_train_pred)
    test_acc = accuracy_score(y_test_risk, risk_test_pred)

    print(f"Risk Model Training Accuracy: {train_acc:.3f}")
    print(f"Risk Model Testing Accuracy: {test_acc:.3f}")

    # ===============================
    # Save Models
    # ===============================

    print("\nSaving models...")

    os.makedirs("app/models", exist_ok=True)

    yield_model_path = "app/models/model.pkl"
    risk_model_path = "app/models/risk_model.pkl"

    joblib.dump(yield_model, yield_model_path)
    joblib.dump(risk_model, risk_model_path)

    print(f"✅ Yield model saved to {yield_model_path}")
    print(f"✅ Risk model saved to {risk_model_path}")

    # ===============================
    # Feature Importance
    # ===============================

    print("\nFeature Importance (Yield Model):")

    feature_importance = pd.DataFrame({
        "feature": X.columns,
        "importance": yield_model.feature_importances_
    }).sort_values(by="importance", ascending=False)

    print(feature_importance.head(10))

    print("\n🎉 Training completed successfully!")


if __name__ == "__main__":
    main()

