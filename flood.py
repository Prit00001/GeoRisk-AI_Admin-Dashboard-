# -*- coding: utf-8 -*-
"""
Flood Prediction Module for Manipur Districts
Uses the ManipurFloodPredictor model for 3-day advance flood prediction
"""

import os
import sys
from datetime import datetime

# Add model_export directory to path
model_dir = os.path.join(os.path.dirname(__file__), 'model_export')
if model_dir not in sys.path:
    sys.path.insert(0, model_dir)

from model_export.manipur_predictor import ManipurFloodPredictor


class FloodPredictor:
    """Wrapper class for flood prediction across Manipur districts"""
    
    def __init__(self):
        """Initialize the flood predictor with model and encoder paths"""
        self.model_path = os.path.join(os.path.dirname(__file__), 'model_export', 'manipur_flood_model.joblib')
        self.encoders_path = os.path.join(os.path.dirname(__file__), 'model_export', 'manipur_encoders.joblib')
        
        # Initialize predictor
        try:
            self.predictor = ManipurFloodPredictor(
                model_path=self.model_path,
                encoders_path=self.encoders_path
            )
            print("✅ Flood model loaded successfully")
        except AttributeError as e:
            if "sklearn" in str(e) or "pickle" in str(e):
                print(f"⚠️ Scikit-learn version mismatch detected.")
                print(f"The model was trained with a different version of scikit-learn.")
                print(f"Original error: {e}")
                print(f"\nTip: Try upgrading scikit-learn: pip install --upgrade scikit-learn")
            raise Exception(f"Model loading failed due to version incompatibility: {e}")
        except Exception as e:
            print(f"❌ Error loading flood model: {e}")
            raise
    
    def predict_flood_risk(self, district_name, rainfall_3days=None, temperature=None, 
                          humidity=None, wind_speed=None, river_water_level=None,
                          soil_moisture=None, drainage_capacity=None, dam_release=None,
                          season=None):
        """
        Predict flood risk for a given district
        
        Args:
            district_name (str): Name of the Manipur district
            rainfall_3days (float): 3-day cumulative rainfall in mm (default: estimated based on season)
            temperature (float): Temperature in °C (default: 25)
            humidity (float): Humidity percentage (default: 75)
            wind_speed (float): Wind speed in km/h (default: 10)
            river_water_level (float): River water level in meters (default: 5)
            soil_moisture (float): Soil moisture percentage (default: 60)
            drainage_capacity (float): Drainage capacity 0-1 (default: 0.5)
            dam_release (int): Dam release status 0/1 (default: 0)
            season (int): Season code 1=Winter, 2=Summer, 3=Monsoon, 4=Post-monsoon (default: auto-detect)
        
        Returns:
            dict: Prediction results with flood_probability, risk_level, etc.
        """
        
        # Auto-detect season if not provided
        if season is None:
            month = datetime.now().month
            if month in [12, 1, 2]:
                season = 1  # Winter
            elif month in [3, 4, 5]:
                season = 2  # Summer
            elif month in [6, 7, 8, 9]:
                season = 3  # Monsoon
            else:
                season = 4  # Post-monsoon
        
        # Set default values based on season
        if rainfall_3days is None:
            rainfall_defaults = {1: 20, 2: 50, 3: 150, 4: 80}
            rainfall_3days = rainfall_defaults.get(season, 50)
        
        if temperature is None:
            temp_defaults = {1: 18, 2: 28, 3: 26, 4: 24}
            temperature = temp_defaults.get(season, 25)
        
        if humidity is None:
            humidity_defaults = {1: 60, 2: 70, 3: 90, 4: 80}
            humidity = humidity_defaults.get(season, 75)
        
        # Set other defaults
        wind_speed = wind_speed or 10
        river_water_level = river_water_level or 5
        soil_moisture = soil_moisture or 60
        drainage_capacity = drainage_capacity or 0.5
        dam_release = dam_release or 0
        
        try:
            # Get prediction from model
            result = self.predictor.predict(
                district_name=district_name,
                rainfall_3days=rainfall_3days,
                temperature=temperature,
                humidity=humidity,
                wind_speed=wind_speed,
                river_water_level=river_water_level,
                soil_moisture=soil_moisture,
                drainage_capacity=drainage_capacity,
                dam_release=dam_release,
                season=season
            )
            
            # Add input parameters to result
            result['inputs'] = {
                'rainfall_3days': rainfall_3days,
                'temperature': temperature,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'river_water_level': river_water_level,
                'soil_moisture': soil_moisture,
                'drainage_capacity': drainage_capacity,
                'dam_release': dam_release,
                'season': season
            }
            
            return result
            
        except Exception as e:
            return {
                'error': str(e),
                'district': district_name,
                'flood_probability': 0,
                'risk_level': 'ERROR',
                'risk_emoji': '⚠️'
            }
    
    def get_available_districts(self):
        """Get list of all available districts"""
        return list(self.predictor.MANIPUR_DISTRICTS.keys())
    
    def get_district_info(self, district_name):
        """Get information about a specific district"""
        if district_name in self.predictor.MANIPUR_DISTRICTS:
            return self.predictor.MANIPUR_DISTRICTS[district_name]
        return None


# Convenience function for quick predictions
def predict_flood(district_name, **kwargs):
    """
    Quick flood prediction function
    
    Usage:
        result = predict_flood('Imphal West', rainfall_3days=120, humidity=85)
    """
    predictor = FloodPredictor()
    return predictor.predict_flood_risk(district_name, **kwargs)


# Test function
if __name__ == "__main__":
    print("🌊 Testing Flood Prediction Module\n")
    
    # Initialize predictor
    predictor = FloodPredictor()
    
    # Test prediction for a high-risk scenario
    print("Testing HIGH RISK scenario (Monsoon in Thoubal):")
    result = predictor.predict_flood_risk(
        district_name='Thoubal',
        rainfall_3days=180,
        temperature=26,
        humidity=95,
        river_water_level=8,
        season=3  # Monsoon
    )
    
    print(f"District: {result['district']}")
    print(f"Flood Probability: {result['flood_probability']:.1%}")
    print(f"Risk Level: {result['risk_emoji']} {result['risk_level']}")
    print(f"Prediction: {result['prediction']}")
    if result.get('warnings'):
        print(f"Warnings: {', '.join(result['warnings'])}")
    
    print("\n" + "="*50 + "\n")
    
    # Test prediction for a low-risk scenario
    print("Testing LOW RISK scenario (Winter in Ukhrul):")
    result2 = predictor.predict_flood_risk(
        district_name='Ukhrul',
        rainfall_3days=20,
        temperature=15,
        humidity=60,
        river_water_level=3,
        season=1  # Winter
    )
    
    print(f"District: {result2['district']}")
    print(f"Flood Probability: {result2['flood_probability']:.1%}")
    print(f"Risk Level: {result2['risk_emoji']} {result2['risk_level']}")
    print(f"Prediction: {result2['prediction']}")
    
    print("\n✅ Flood prediction module working correctly!")