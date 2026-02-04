# Landslide Prediction Model Package

**Version:** 1.0.0  
**Export Date:** 2026-01-27  
**Region:** Manipur, India  
**Prediction Horizon:** 3 days ahead

## Contents

```
model_package/
├── models/                    # Trained model files
│   ├── random_forest_model.pkl
│   ├── xgboost_model.pkl
│   ├── neural_network_model.pkl
│   ├── scaler.pkl
│   ├── feature_names.pkl
│   └── best_threshold.pkl
├── prediction_api.py          # Python API for predictions
├── model_metadata.json        # Model information
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Verify installation:**
```python
from prediction_api import LandslidePredictor
predictor = LandslidePredictor()
```

## Quick Start

### Single Prediction

```python
from prediction_api import LandslidePredictor

# Initialize predictor
predictor = LandslidePredictor(model_dir='models')

# Make prediction
result = predictor.predict(
    lat=24.817,
    lon=93.950,
    rainfall_mm=150.0,        # Rainfall in mm
    slope_angle=35.0,         # Slope in degrees
    soil_saturation=0.85,     # 0-1 scale
    vegetation_cover=0.3,     # 0-1 scale
    earthquake_activity=0.6,  # 0-1 scale
    proximity_to_water=0.4,   # 0-1 scale
    soil_type='Sand'          # 'Gravel', 'Sand', or 'Silt'
)

print(result)
```

### Batch Predictions

```python
import pandas as pd

# Load locations
locations = pd.read_csv('locations.csv')

# Predict for all
results = predictor.batch_predict(locations)

# Filter alerts
alerts = results[results['risk_level'].isin(['HIGH', 'EXTREME'])]
```

## Model Information

- **Features:** 17
- **Optimal Threshold:** 0.640
- **Models:** Random Forest, XGBoost, Neural Network
- **Target:** Binary landslide prediction (3 days ahead)

## Risk Levels

- **EXTREME:** ≥80% probability - Immediate evacuation
- **HIGH:** 60-80% probability - High alert
- **MODERATE:** 40-60% probability - Monitor closely
- **LOW:** 20-40% probability - Stay informed
- **MINIMAL:** <20% probability - Normal conditions

## Input Requirements

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| lat | float | 23.83-25.68 | Latitude (Manipur) |
| lon | float | 93.03-94.78 | Longitude (Manipur) |
| rainfall_mm | float | 0-500 | Rainfall in millimeters |
| slope_angle | float | 0-90 | Slope angle in degrees |
| soil_saturation | float | 0-1 | Soil moisture (0=dry, 1=saturated) |
| vegetation_cover | float | 0-1 | Vegetation density (0=bare, 1=full) |
| earthquake_activity | float | 0-1 | Seismic activity (0=none, 1=high) |
| proximity_to_water | float | 0-1 | Water proximity (0=far, 1=near) |
| soil_type | string | - | 'Gravel', 'Sand', or 'Silt' |

## API Response

```json
{
  "latitude": 24.817,
  "longitude": 93.950,
  "prediction_date": "2026-01-30",
  "landslide_probability": 0.78,
  "risk_level": "HIGH",
  "prediction": "LANDSLIDE WARNING",
  "confidence": "HIGH",
  "timestamp": "2026-01-27T10:30:00"
}
```

## Integration Examples

### REST API Server

```python
from flask import Flask, request, jsonify
from prediction_api import LandslidePredictor

app = Flask(__name__)
predictor = LandslidePredictor()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    result = predictor.predict(**data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Scheduled Monitoring

```python
import schedule
import time

def daily_scan():
    # Your monitoring locations
    locations = get_monitoring_locations()
    results = predictor.batch_predict(locations)
    
    # Send alerts
    alerts = results[results['risk_level'].isin(['HIGH', 'EXTREME'])]
    if not alerts.empty:
        send_alerts(alerts)

schedule.every().day.at("06:00").do(daily_scan)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Performance

- **Inference Time:** ~50ms per prediction
- **Memory:** ~200MB loaded
- **Accuracy:** See model_metadata.json for metrics

## License & Support

This model is for disaster prediction and public safety.
Use responsibly and validate predictions with local expertise.

## Version History

- **1.0.0** (2026-01-27): Initial export
