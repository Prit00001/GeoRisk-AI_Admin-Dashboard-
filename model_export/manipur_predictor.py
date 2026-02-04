# -*- coding: utf-8 -*-
"""
Manipur Flood Prediction - Deployment Class
"""

import numpy as np
import joblib

class ManipurFloodPredictor:
    def __init__(self, model_path, encoders_path, scaler_path=None):
        self.model = joblib.load(model_path)
        encoders_data = joblib.load(encoders_path)
        self.district_encoder = encoders_data['district_encoder']
        self.type_encoder = encoders_data['type_encoder']
        self.MANIPUR_DISTRICTS = encoders_data['district_info']
        self.feature_columns = encoders_data['feature_columns']
        self.best_model_name = encoders_data['best_model_name']
        self.scaler = joblib.load(scaler_path) if scaler_path else None
        
    def predict(self, district_name, rainfall_3days, temperature, humidity, 
                wind_speed, river_water_level, soil_moisture, drainage_capacity,
                dam_release, season, deforestation_index=0.3, 
                encroachment_level=0.3, previous_floods=0):
        
        if district_name not in self.MANIPUR_DISTRICTS:
            return {"error": f"District not found"}
        
        district_info = self.MANIPUR_DISTRICTS[district_name]
        
        input_dict = {
            'rainfall_3days': rainfall_3days,
            'temperature': temperature,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'elevation': district_info['avg_elevation'],
            'distance_to_river': 2 if district_info['type'] == 'valley' else 5,
            'slope': 5 if district_info['type'] == 'valley' else 25,
            'river_water_level': river_water_level,
            'soil_moisture': soil_moisture,
            'drainage_capacity': drainage_capacity,
            'dam_release': dam_release,
            'previous_floods': previous_floods,
            'season': season,
            'deforestation_index': deforestation_index,
            'encroachment_level': encroachment_level,
            'district_encoded': self.district_encoder.transform([district_name])[0],
            'district_type_encoded': self.type_encoder.transform([district_info['type']])[0]
        }
        
        input_data = np.array([[input_dict[col] for col in self.feature_columns]])
        
        if self.scaler and self.best_model_name == 'Logistic Regression':
            input_data = self.scaler.transform(input_data)
        
        flood_prob = self.model.predict_proba(input_data)[0, 1]
        prediction = "FLOOD WARNING" if flood_prob > 0.5 else "No Flood Expected"
        
        if flood_prob > 0.7:
            risk_level = "CRITICAL"
            risk_emoji = "🔴"
        elif flood_prob > 0.5:
            risk_level = "HIGH"
            risk_emoji = "🟠"
        elif flood_prob > 0.3:
            risk_level = "MODERATE"
            risk_emoji = "🟡"
        else:
            risk_level = "LOW"
            risk_emoji = "🟢"
        
        warnings = []
        if district_info['type'] == 'valley' and rainfall_3days > 100:
            warnings.append("Valley district at high risk")
        if river_water_level > 7:
            warnings.append("River level critical")
        
        return {
            'district': district_name,
            'flood_probability': float(flood_prob),
            'prediction': prediction,
            'risk_level': risk_level,
            'risk_emoji': risk_emoji,
            'warnings': warnings
        }
