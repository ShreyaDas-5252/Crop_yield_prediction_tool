# scripts/generate_sample_data.py
import numpy as np
import pandas as pd
import os

os.makedirs('data/processed', exist_ok=True)

np.random.seed(42)
n = 3000

crops = ['wheat', 'rice', 'maize', 'soybean', 'sugarcane']
crop = np.random.choice(crops, size=n)
rainfall = np.random.normal(loc=600, scale=250, size=n).clip(0, 3000)
temperature = np.random.normal(loc=25, scale=6, size=n).clip(-5, 45)
humidity = np.random.normal(loc=65, scale=15, size=n).clip(10, 100)
soil_ph = np.random.normal(loc=6.5, scale=0.8, size=n).clip(3.5, 9.0)
fertilizer = np.random.normal(loc=150, scale=80, size=n).clip(0, 800)

base = {'wheat': 3.0, 'rice': 4.0, 'maize': 5.0, 'soybean': 2.2, 'sugarcane': 60.0}
y = []
for i in range(n):
    c = crop[i]
    r = rainfall[i]
    t = temperature[i]
    h = humidity[i]
    p = soil_ph[i]
    f = fertilizer[i]
    crop_base = base[c]
    rain_factor = 1 - np.exp(-r / 400)
    temp_factor = np.exp(-((t - 25) ** 2) / 60)
    hum_factor = 1 - abs(h - 65) / 120
    ph_factor = 1 - ((p - 6.5) ** 2) / 9
    fert_factor = 1 - np.exp(-f / 120)
    noise = np.random.normal(0, 0.15 * crop_base)
    yield_val = crop_base * (0.5 + 0.8 * rain_factor * temp_factor * hum_factor * ph_factor * fert_factor) + noise
    y.append(max(0.1, yield_val))

df = pd.DataFrame({
    'crop': crop,
    'rainfall_mm': rainfall.round(1),
    'temperature_c': temperature.round(2),
    'humidity_percent': humidity.round(1),
    'soil_ph': soil_ph.round(2),
    'fertilizer_kg_per_ha': fertilizer.round(1),
    'yield_t_per_ha': np.round(y, 3)
})

df.to_csv('data/processed/sample_crop_data.csv', index=False)
print('Saved sample dataset to data/processed/sample_crop_data.csv (rows: {})'.format(len(df)))
