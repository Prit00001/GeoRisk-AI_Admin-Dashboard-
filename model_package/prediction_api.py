"""
LANDSLIDE PREDICTION API
========================

Simple API for making predictions with the exported model.

USAGE:
------
from prediction_api import LandslidePredictor

# Initialize predictor
predictor = LandslidePredictor(model_dir='models')

# Make prediction
result = predictor.predict(
    lat=24.817,
    lon=93.950,
    rainfall_mm=150.0,
    slope_angle=35.0,
    soil_saturation=0.85,
    vegetation_cover=0.3,
    earthquake_activity=0.6,
    proximity_to_water=0.4,
    soil_type='Sand'  # 'Gravel', 'Sand', or 'Silt'
)

print(result)
# {'risk_level': 'HIGH', 'probability': 0.78, 'prediction': 'WARNING', ...}
"""

import numpy as np
import pandas as pd
import joblib
from datetime import datetime, timedelta


class LandslidePredictor:
    """Production-ready landslide prediction API"""
    
    def __init__(self, model_dir='models'):
        """Load trained models"""
        print("Loading models...")
        
        self.scaler = joblib.load(f'{model_dir}/scaler.pkl')
        self.feature_names = joblib.load(f'{model_dir}/feature_names.pkl')
        self.threshold = joblib.load(f'{model_dir}/best_threshold.pkl')
        
        self.models = {
            'random_forest': joblib.load(f'{model_dir}/random_forest_model.pkl'),
            'xgboost': joblib.load(f'{model_dir}/xgboost_model.pkl'),
            'neural_network': joblib.load(f'{model_dir}/neural_network_model.pkl')
        }
        
        print(f"[OK] Models loaded successfully (threshold: {self.threshold:.3f})")
    
    def engineer_features(self, df):
        """Feature engineering"""
        df = df.copy()
        
        df['rainfall_slope_interaction'] = df['Rainfall_mm'] * df['Slope_Angle']
        df['saturation_slope_risk'] = df['Soil_Saturation'] * df['Slope_Angle']
        df['rainfall_saturation'] = df['Rainfall_mm'] * df['Soil_Saturation']
        
        df['hydrological_risk'] = (df['Rainfall_mm'] * 0.4 + 
                                    df['Soil_Saturation'] * 0.4 + 
                                    df['Proximity_to_Water'] * 0.2)
        
        df['geological_risk'] = (df['Slope_Angle'] * 0.5 + 
                                  df['Earthquake_Activity'] * 0.3 +
                                  (1 - df['Vegetation_Cover']) * 0.2)
        
        df['rainfall_squared'] = df['Rainfall_mm'] ** 2
        df['slope_squared'] = df['Slope_Angle'] ** 2
        df['stability_index'] = df['Vegetation_Cover'] / (df['Slope_Angle'] + 1)
        
        return df
    
    def classify_risk(self, probability):
        """Classify risk level"""
        if probability >= 0.8:
            return 'EXTREME'
        elif probability >= 0.6:
            return 'HIGH'
        elif probability >= 0.4:
            return 'MODERATE'
        elif probability >= 0.2:
            return 'LOW'
        else:
            return 'MINIMAL'
    
    def predict(self, lat, lon, rainfall_mm, slope_angle, soil_saturation,
                vegetation_cover, earthquake_activity, proximity_to_water,
                soil_type='Sand', prediction_days=3):
        """
        Make landslide prediction
        
        Args:
            lat: Latitude
            lon: Longitude
            rainfall_mm: Rainfall in millimeters (0-500)
            slope_angle: Slope angle in degrees (0-90)
            soil_saturation: Soil moisture 0-1 (0=dry, 1=saturated)
            vegetation_cover: Vegetation cover 0-1 (0=bare, 1=full)
            earthquake_activity: Seismic activity 0-1 (0=none, 1=high)
            proximity_to_water: Distance to water 0-1 (0=far, 1=near)
            soil_type: 'Gravel', 'Sand', or 'Silt'
            prediction_days: Days ahead to predict (default 3)
        
        Returns:
            dict with prediction results
        """
        
        # Prepare input features
        features = {
            'Rainfall_mm': rainfall_mm,
            'Slope_Angle': slope_angle,
            'Soil_Saturation': soil_saturation,
            'Vegetation_Cover': vegetation_cover,
            'Earthquake_Activity': earthquake_activity,
            'Proximity_to_Water': proximity_to_water,
            'Soil_Type_Gravel': 1 if soil_type == 'Gravel' else 0,
            'Soil_Type_Sand': 1 if soil_type == 'Sand' else 0,
            'Soil_Type_Silt': 1 if soil_type == 'Silt' else 0
        }
        
        # Create DataFrame
        df = pd.DataFrame([features])
        
        # Engineer features
        df_engineered = self.engineer_features(df)
        
        # Ensure all features present
        X = df_engineered[self.feature_names]
        
        # Get ensemble prediction
        predictions = []
        for model in self.models.values():
            pred_proba = model.predict_proba(X)[:, 1]
            predictions.append(pred_proba[0])
        
        probability = np.mean(predictions)
        risk_level = self.classify_risk(probability)
        
        # Create result
        result = {
            'latitude': lat,
            'longitude': lon,
            'prediction_date': (datetime.now() + timedelta(days=prediction_days)).strftime('%Y-%m-%d'),
            'landslide_probability': float(probability),
            'risk_level': risk_level,
            'prediction': 'LANDSLIDE WARNING' if probability >= self.threshold else 'SAFE',
            'confidence': 'HIGH' if max(predictions) - min(predictions) < 0.15 else 'MEDIUM',
            'timestamp': datetime.now().isoformat(),
            'input_features': features
        }
        
        return result
    
    def batch_predict(self, locations_df):
        """
        Predict for multiple locations
        
        Args:
            locations_df: DataFrame with columns matching predict() parameters
        
        Returns:
            DataFrame with predictions
        """
        results = []
        
        for _, row in locations_df.iterrows():
            result = self.predict(
                lat=row['lat'],
                lon=row['lon'],
                rainfall_mm=row['rainfall_mm'],
                slope_angle=row['slope_angle'],
                soil_saturation=row['soil_saturation'],
                vegetation_cover=row['vegetation_cover'],
                earthquake_activity=row['earthquake_activity'],
                proximity_to_water=row['proximity_to_water'],
                soil_type=row.get('soil_type', 'Sand')
            )
            results.append(result)
        
        return pd.DataFrame(results)


# Example usage
if __name__ == "__main__":
    # Initialize predictor
    predictor = LandslidePredictor()
    
    # Single prediction
    print("\n" + "="*70)
    print("EXAMPLE PREDICTION")
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
    print(f"Confidence: {result['confidence']}")
    print(f"Target Date: {result['prediction_date']}")
