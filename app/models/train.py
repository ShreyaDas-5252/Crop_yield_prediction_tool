import sys
import os
# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
from app.utils.preprocessing import load_data, prepare_features, train_test_split_df

def main():
    """Train the crop yield prediction model"""
    print("Loading data...")
    
    # Provide the path to your data file
    data_path = "data/processed/sample_crop_data.csv"
    df = load_data(data_path)
    
    if df is None or df.empty:
        print("Error: No data loaded!")
        return
    
    print("Preprocessing features...")
    X, y = prepare_features(df)
    
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split_df(X, y)
    
    print("Training model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"Training R²: {train_score:.3f}")
    print(f"Testing R²: {test_score:.3f}")
    
    # Save model
    os.makedirs("app/models", exist_ok=True)
    joblib.dump(model, "app/models/model.pkl")
    print("Model saved to app/models/model.pkl")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 10 Feature Importance:")
    print(feature_importance.head(10))

if __name__ == "__main__":
    main()