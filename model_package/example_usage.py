"""
Example usage of the exported model
"""

from prediction_api import LandslidePredictor
import pandas as pd

# Initialize predictor
print("Initializing model...")
predictor = LandslidePredictor()

# Example 1: Single prediction
print("\n" + "="*70)
print("EXAMPLE 1: Single Location Prediction")
print("="*70)

result = predictor.predict(
    lat=24.817,
    lon=93.950,
    rainfall_mm=150.0,
    slope_angle=35.0,
    soil_saturation=0.85,
    vegetation_cover=0.3,
    earthquake_activity=0.6,
    proximity_to_water=0.4,
    soil_type='Sand'
)

print(f"\nLocation: ({result['latitude']}, {result['longitude']})")
print(f"Risk Level: {result['risk_level']}")
print(f"Probability: {result['landslide_probability']:.2%}")
print(f"Prediction: {result['prediction']}")

# Example 2: Batch prediction
print("\n" + "="*70)
print("EXAMPLE 2: Batch Prediction")
print("="*70)

locations_data = {
    'lat': [24.817, 25.123, 24.234],
    'lon': [93.950, 94.456, 93.678],
    'rainfall_mm': [150, 180, 120],
    'slope_angle': [35, 42, 28],
    'soil_saturation': [0.85, 0.90, 0.75],
    'vegetation_cover': [0.3, 0.2, 0.5],
    'earthquake_activity': [0.6, 0.7, 0.4],
    'proximity_to_water': [0.4, 0.6, 0.3],
    'soil_type': ['Sand', 'Gravel', 'Silt']
}

locations_df = pd.DataFrame(locations_data)
results = predictor.batch_predict(locations_df)

print(f"\nProcessed {len(results)} locations")
print(f"\nAlerts (HIGH or EXTREME risk):")
alerts = results[results['risk_level'].isin(['HIGH', 'EXTREME'])]
print(alerts[['latitude', 'longitude', 'risk_level', 'landslide_probability']].to_string(index=False))
