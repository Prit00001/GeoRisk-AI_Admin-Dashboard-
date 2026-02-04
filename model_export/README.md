# Manipur Flood Prediction Model

Machine learning model for 3-day advance flood prediction across Manipur's 16 districts.

## Quick Start

```python
from manipur_predictor import ManipurFloodPredictor

predictor = ManipurFloodPredictor(
    model_path='manipur_flood_model.joblib',
    encoders_path='manipur_encoders.joblib'
)

result = predictor.predict(
    district_name='Thoubal',
    rainfall_3days=150,
    temperature=26,
    humidity=90,
    wind_speed=12,
    river_water_level=8.5,
    soil_moisture=85,
    drainage_capacity=0.4,
    dam_release=1,
    season=2
)

print(f"Flood Probability: {result['flood_probability']:.1%}")
print(f"Risk Level: {result['risk_emoji']} {result['risk_level']}")
```

## Model Type
Gradient Boosting

## Features
17 input features

## Districts Covered
All 16 Manipur districts (6 valley, 10 hill)
