import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os

def load_data(path="data/processed/sample_crop_data.csv"):
    """Load the crop yield dataset"""
    try:
        if not os.path.exists(path):
            print(f"Data file not found: {path}")
            return None
        
        df = pd.read_csv(path)
        print(f"Loaded dataset with {len(df)} rows and {len(df.columns)} columns")
        print(f"Columns in dataset: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def prepare_features(df):
    """Prepare features and target variable"""
    df_processed = df.copy()
    
    print(f"Available columns: {list(df_processed.columns)}")
    
    # Check what target column exists
    target_columns = ['yield_kg_per_ha', 'yield', 'production', 'yield_tons_per_ha']
    target_col = None
    
    for col in target_columns:
        if col in df_processed.columns:
            target_col = col
            break
    
    if target_col is None:
        target_col = df_processed.columns[-1]
        print(f"No standard target column found. Using '{target_col}' as target.")
    
    print(f"Using target column: {target_col}")
    
    # Handle categorical variables
    categorical_cols = ['crop_type', 'soil_type', 'irrigation', 'crop']
    label_encoders = {}
    
    for col in categorical_cols:
        if col in df_processed.columns:
            le = LabelEncoder()
            df_processed[col] = le.fit_transform(df_processed[col].astype(str))
            label_encoders[col] = le
    
    # Define possible feature columns
    possible_features = ['crop_type', 'crop', 'rainfall', 'temperature', 'humidity', 
                        'soil_ph', 'fertilizer_kg_per_ha', 'soil_type', 'irrigation',
                        'fertilizer', 'ph', 'temp']
    
    # Use only columns that exist in the dataframe and are not the target
    available_features = [col for col in possible_features 
                         if col in df_processed.columns and col != target_col]
    
    print(f"Using features: {available_features}")
    
    X = df_processed[available_features]
    
    # Convert target to tons/ha if it's in kg/ha
    if 'kg' in target_col.lower() or df_processed[target_col].max() > 10000:
        y = df_processed[target_col] / 1000  # Convert kg/ha to tons/ha
        print("Converted target from kg/ha to tons/ha")
    else:
        y = df_processed[target_col]
    
    print(f"Target statistics - Min: {y.min():.2f}, Max: {y.max():.2f}, Mean: {y.mean():.2f}")
    
    return X, y

def train_test_split_df(X, y, test_size=0.2, random_state=42):
    """Split data into train and test sets"""
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def preprocess_input(input_data):
    """Preprocess user input for prediction"""
    # Convert input data to DataFrame
    input_df = pd.DataFrame([input_data])
    
    # Handle categorical encoding (simplified version)
    categorical_mapping = {
        'crop_type': {'Wheat': 0, 'Rice': 1, 'Corn': 2, 'Soybean': 3, 'Cotton': 4, 'Sugarcane': 5},
        'soil_type': {'Loamy': 0, 'Sandy': 1, 'Clay': 2, 'Silty': 3, 'Peaty': 4, 'Chalky': 5},
        'irrigation': {'Drip': 0, 'Sprinkler': 1, 'Flood': 2, 'None': 3}
    }
    
    for col, mapping in categorical_mapping.items():
        if col in input_df.columns:
            input_df[col] = input_df[col].map(mapping)
            # Fill any NaN values with 0 (for unknown categories)
            input_df[col] = input_df[col].fillna(0)
    
    return input_df