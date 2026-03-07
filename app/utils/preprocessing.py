import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


# ==========================================
# Load Dataset
# ==========================================

def load_data(path="data/processed/sample_crop_data.csv"):
    """
    Load crop dataset
    """

    try:

        if not os.path.exists(path):
            print(f"Dataset not found: {path}")
            return None

        df = pd.read_csv(path)

        print("Dataset loaded successfully")
        print(f"Rows: {len(df)}")
        print(f"Columns: {len(df.columns)}")
        print(f"Column names: {list(df.columns)}")

        return df

    except Exception as e:

        print(f"Error loading dataset: {e}")
        return None


# ==========================================
# Feature Preparation
# ==========================================

def prepare_features(df):
    """
    Prepare features and target variable
    """

    df_processed = df.copy()

    # --------------------------------------
    # Expected columns in advanced dataset
    # --------------------------------------

    expected_features = [

        "crop",
        "state",
        "season",

        "rainfall_mm",
        "temperature_c",
        "humidity_percent",

        "soil_ph",
        "soil_nitrogen",
        "soil_phosphorus",
        "soil_potassium",

        "soil_moisture",
        "solar_radiation",

        "ndvi",
        "irrigation_level"

    ]

    # --------------------------------------
    # Check which columns exist
    # --------------------------------------

    available_features = []

    for col in expected_features:

        if col in df_processed.columns:
            available_features.append(col)

    print("Using features:")
    print(available_features)

    # --------------------------------------
    # Encode categorical variables
    # --------------------------------------

    categorical_cols = ["crop", "state", "season"]

    label_encoders = {}

    for col in categorical_cols:

        if col in df_processed.columns:

            le = LabelEncoder()

            df_processed[col] = le.fit_transform(
                df_processed[col].astype(str)
            )

            label_encoders[col] = le

    # --------------------------------------
    # Select features
    # --------------------------------------

    X = df_processed[available_features]

    # --------------------------------------
    # Select target variable
    # --------------------------------------

    target_columns = [

        "yield_t_per_ha",
        "yield_kg_per_ha",
        "yield"

    ]

    target_col = None

    for col in target_columns:

        if col in df_processed.columns:
            target_col = col
            break

    if target_col is None:

        raise ValueError(
            "No yield column found in dataset."
        )

    print(f"Target column used: {target_col}")

    y = df_processed[target_col]

    # --------------------------------------
    # Convert kg/ha to ton/ha if necessary
    # --------------------------------------

    if "kg" in target_col:

        y = y / 1000
        print("Converted yield from kg/ha to ton/ha")

    # --------------------------------------
    # Basic dataset statistics
    # --------------------------------------

    print("Yield Statistics")
    print(f"Min: {y.min():.2f}")
    print(f"Max: {y.max():.2f}")
    print(f"Mean: {y.mean():.2f}")

    return X, y


# ==========================================
# Train Test Split
# ==========================================

def train_test_split_df(X, y, test_size=0.2):

    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=42
    )


# ==========================================
# Preprocess User Input
# ==========================================

def preprocess_input(input_data):

    """
    Convert user input into model-ready format
    """

    input_df = pd.DataFrame([input_data])

    categorical_mapping = {

        "crop": {

            "Rice": 0,
            "Wheat": 1,
            "Maize": 2,
            "Soybean": 3,
            "Sugarcane": 4,
            "Cotton": 5

        },

        "state": {

            "Punjab": 0,
            "Haryana": 1,
            "Uttar Pradesh": 2,
            "Bihar": 3,
            "Maharashtra": 4,
            "Karnataka": 5

        },

        "season": {

            "Kharif": 0,
            "Rabi": 1,
            "Zaid": 2

        }

    }

    for col, mapping in categorical_mapping.items():

        if col in input_df.columns:

            input_df[col] = input_df[col].map(mapping)

            input_df[col] = input_df[col].fillna(0)

    return input_df