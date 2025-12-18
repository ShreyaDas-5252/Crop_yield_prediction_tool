import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "harsh@618"),
    "database": os.getenv("DB_NAME", "crop_yield"),
    "port": int(os.getenv("DB_PORT", 3306))
}

# Model Configuration
MODEL_CONFIG = {
    "model_path": "app/models/model.pkl",
    "retrain_days": 30,
    "confidence_threshold": 0.85
}

# API Configuration
API_CONFIG = {
    "weather_api_key": os.getenv("WEATHER_API_KEY", ""),
    "soil_api_key": os.getenv("SOIL_API_KEY", ""),
    "market_api_key": os.getenv("MARKET_API_KEY", "")
}

# App Configuration
APP_CONFIG = {
    "name": "Crop Yield Pro",
    "version": "2.0.0",
    "debug": os.getenv("DEBUG", "False").lower() == "true"
}

# Feature Configuration
FEATURES = {
    "basic": ["rainfall", "temperature", "humidity", "soil_ph", "fertilizer_kg_per_ha"],
    "advanced": ["rainfall", "temperature", "humidity", "soil_ph", "fertilizer_kg_per_ha",
                "soil_type", "crop_type", "irrigation", "sunlight_hours", 
                "pesticide_usage", "farm_size", "elevation", "wind_speed"]
}

# Crop Types
CROP_TYPES = [
    "Wheat", "Rice", "Corn", "Soybean", "Cotton", "Sugarcane",
    "Potato", "Tomato", "Barley", "Oats", "Millet", "Sorghum"
]

# Soil Types
SOIL_TYPES = ["Loamy", "Sandy", "Clay", "Silty", "Peaty", "Chalky"]

# Irrigation Types
IRRIGATION_TYPES = ["Drip", "Sprinkler", "Flood", "None"]

# Data Paths
DATA_PATH = "data/processed/sample_crop_data.csv"
MODEL_PATH = "app/models/model.pkl"