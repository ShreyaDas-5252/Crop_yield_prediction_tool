import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import xgboost as xgb
import os

class AdvancedYieldPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.is_trained = False
        
    def create_model(self):
        """Create an ensemble model"""
        from sklearn.ensemble import VotingRegressor
        
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
        xg = xgb.XGBRegressor(n_estimators=100, random_state=42)
        
        self.model = VotingRegressor([
            ('rf', rf),
            ('gb', gb),
            ('xg', xg)
        ])
    
    def preprocess_features(self, X, training=False):
        """Preprocess features for training/prediction"""
        X_processed = X.copy()
        
        # Encode categorical variables
        categorical_columns = ['crop_type', 'soil_type', 'irrigation']
        
        for col in categorical_columns:
            if col in X_processed.columns:
                if training:
                    self.label_encoders[col] = LabelEncoder()
                    X_processed[col] = self.label_encoders[col].fit_transform(X_processed[col])
                else:
                    if col in self.label_encoders:
                        # Handle unseen labels
                        known_labels = set(self.label_encoders[col].classes_)
                        current_labels = set(X_processed[col].unique())
                        unseen_labels = current_labels - known_labels
                        
                        if unseen_labels:
                            # Replace unseen labels with most frequent
                            most_frequent = self.label_encoders[col].classes_[0]
                            X_processed[col] = X_processed[col].apply(
                                lambda x: x if x in known_labels else most_frequent
                            )
                        
                        X_processed[col] = self.label_encoders[col].transform(X_processed[col])
        
        # Scale numerical features
        numerical_columns = ['rainfall', 'temperature', 'humidity', 'soil_ph', 
                           'fertilizer_kg_per_ha', 'sunlight_hours', 'pesticide_usage',
                           'farm_size', 'elevation']
        
        numerical_columns = [col for col in numerical_columns if col in X_processed.columns]
        
        if training:
            X_processed[numerical_columns] = self.scaler.fit_transform(X_processed[numerical_columns])
        else:
            if hasattr(self.scaler, 'mean_'):
                X_processed[numerical_columns] = self.scaler.transform(X_processed[numerical_columns])
        
        return X_processed
    
    def train(self, X, y):
        """Train the model"""
        if self.model is None:
            self.create_model()
        
        X_processed = self.preprocess_features(X, training=True)
        
        self.model.fit(X_processed, y)
        self.is_trained = True
        
        # Calculate training score
        y_pred = self.model.predict(X_processed)
        mae = mean_absolute_error(y, y_pred)
        r2 = r2_score(y, y_pred)
        
        print(f"Training completed - MAE: {mae:.3f}, R²: {r2:.3f}")
        
        return mae, r2
    
    def predict(self, X):
        """Make predictions"""
        if not self.is_trained:
            # Load pre-trained model or use fallback
            return self.fallback_prediction(X)
        
        X_processed = self.preprocess_features(X, training=False)
        
        predictions = self.model.predict(X_processed)
        confidence = self.calculate_confidence(predictions)
        
        return predictions[0], confidence
    
    def calculate_confidence(self, predictions):
        """Calculate prediction confidence"""
        # Simple confidence calculation based on prediction range
        if len(predictions) > 1:
            std_dev = np.std(predictions)
            confidence = max(0, 1 - std_dev / np.mean(predictions))
        else:
            confidence = 0.85  # Default confidence
        
        return min(confidence, 0.99)
    
    def fallback_prediction(self, X):
        """Fallback prediction when model is not trained"""
        # Simple rule-based fallback
        base_yields = {
            'Wheat': 3.0, 'Rice': 4.0, 'Corn': 3.5, 
            'Soybean': 2.5, 'Cotton': 1.5, 'Sugarcane': 70.0
        }
        
        crop = X['crop_type'].iloc[0] if hasattr(X, 'iloc') else X.get('crop_type', 'Wheat')
        base_yield = base_yields.get(crop, 3.0)
        
        # Simple adjustments based on conditions
        adjustment = 1.0
        
        if X.get('soil_ph', 6.5) < 5.5 or X.get('soil_ph', 6.5) > 7.5:
            adjustment *= 0.8
        
        if X.get('rainfall', 500) < 300:
            adjustment *= 0.7
        elif X.get('rainfall', 500) > 1000:
            adjustment *= 0.9
        
        predicted_yield = base_yield * adjustment
        
        return predicted_yield, 0.7
    
    def save_model(self, filepath):
        """Save the trained model"""
        if self.is_trained:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'label_encoders': self.label_encoders,
                'is_trained': self.is_trained
            }
            joblib.dump(model_data, filepath)
            print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load a trained model"""
        if os.path.exists(filepath):
            model_data = joblib.load(filepath)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.label_encoders = model_data['label_encoders']
            self.is_trained = model_data['is_trained']
            print(f"Model loaded from {filepath}")
        else:
            print(f"Model file not found: {filepath}")

# Singleton instance
advanced_predictor = AdvancedYieldPredictor()