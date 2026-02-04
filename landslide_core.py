

import requests
import sys
import os
import zipfile
from datetime import datetime, timedelta
import pandas as pd
import time

class FreeAPIDataFetcher:
    """Fetch environmental data from FREE APIs only (no keys needed)"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Landslide-Prediction-System/1.0'
        })
    
    def get_weather_open_meteo(self, lat, lon):
        """Get weather from Open-Meteo - completely free, no key needed!"""
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                'latitude': lat,
                'longitude': lon,
                'current': 'temperature_2m,relative_humidity_2m,precipitation,soil_moisture_0_to_1cm',
                'daily': 'precipitation_sum,precipitation_probability_max',
                'timezone': 'Asia/Kolkata',
                'forecast_days': 3
            }
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            current = data.get('current', {})
            daily = data.get('daily', {})
            
            rainfall_forecast = sum(daily.get('precipitation_sum', [0, 0, 0])[:3])
            current_rain = current.get('precipitation', 0)
            total_rainfall = max(current_rain * 24, rainfall_forecast)
            
            humidity = current.get('relative_humidity_2m', 70) / 100.0
            soil_moisture = current.get('soil_moisture_0_to_1cm', humidity)
            
            return {
                'rainfall_mm': float(total_rainfall) if total_rainfall > 0 else 80.0,
                'soil_saturation': float(min(soil_moisture / 100.0 if soil_moisture > 1 else soil_moisture, 1.0)),
                'humidity': float(humidity),
                'temperature': current.get('temperature_2m', 25),
                'success': True
            }
        
        except Exception as e:
            return {
                'rainfall_mm': 100.0,
                'soil_saturation': 0.7,
                'humidity': 0.7,
                'success': False
            }
    
    def get_elevation_slope(self, lat, lon):
        """Get elevation and calculate slope - completely free!"""
        try:
            points = [
                {'latitude': lat, 'longitude': lon},
                {'latitude': lat + 0.002, 'longitude': lon},
                {'latitude': lat - 0.002, 'longitude': lon},
                {'latitude': lat, 'longitude': lon + 0.002},
                {'latitude': lat, 'longitude': lon - 0.002},
            ]
            
            url = "https://api.open-elevation.com/api/v1/lookup"
            response = self.session.post(url, json={'locations': points}, timeout=20)
            response.raise_for_status()
            data = response.json()
            
            elevations = [result['elevation'] for result in data['results']]
            center_elev = elevations[0]
            
            max_diff = max(abs(e - center_elev) for e in elevations[1:])
            distance = 222
            
            if distance > 0:
                slope_ratio = max_diff / distance
                slope_angle = min(abs(slope_ratio) * 45, 60)
            else:
                slope_angle = 20.0
            
            return {
                'elevation': float(center_elev),
                'slope_angle': float(slope_angle),
                'success': True
            }
        
        except Exception as e:
            return {
                'elevation': 500.0,
                'slope_angle': 25.0,
                'success': False
            }
    
    def get_earthquake_activity(self, lat, lon, radius_km=100):
        """Get earthquake data from USGS - completely free!"""
        try:
            url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
            params = {
                'format': 'geojson',
                'latitude': lat,
                'longitude': lon,
                'maxradiuskm': radius_km,
                'starttime': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'minmagnitude': 2.0,
                'orderby': 'magnitude'
            }
            
            response = self.session.get(url, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()
            
            earthquakes = data.get('features', [])
            
            if earthquakes:
                magnitudes = [eq['properties']['mag'] for eq in earthquakes]
                max_mag = max(magnitudes)
                count = len(earthquakes)
                
                mag_score = min(max_mag / 7.0, 1.0)
                freq_score = min(count / 20.0, 1.0)
                activity = (mag_score * 0.7 + freq_score * 0.3)
                
                return {
                    'earthquake_activity': float(activity),
                    'earthquake_count': count,
                    'max_magnitude': float(max_mag),
                    'success': True
                }
            else:
                return {
                    'earthquake_activity': 0.1,
                    'earthquake_count': 0,
                    'max_magnitude': 0.0,
                    'success': True
                }
        
        except Exception as e:
            return {
                'earthquake_activity': 0.3,
                'earthquake_count': 0,
                'success': False
            }
    
    def get_water_proximity(self, lat, lon):
        """Get water proximity from OpenStreetMap - completely free!"""
        try:
            overpass_url = "https://overpass-api.de/api/interpreter"
            query = f"""
            [out:json][timeout:15];
            (
              way["natural"="water"](around:10000,{lat},{lon});
              way["waterway"](around:10000,{lat},{lon});
              relation["natural"="water"](around:10000,{lat},{lon});
            );
            out center 10;
            """
            
            response = self.session.post(
                overpass_url, 
                data={'data': query},
                timeout=20
            )
            response.raise_for_status()
            data = response.json()
            
            elements = data.get('elements', [])
            
            if elements:
                min_distance = float('inf')
                
                for element in elements[:10]:
                    if 'center' in element:
                        water_lat = element['center']['lat']
                        water_lon = element['center']['lon']
                    elif 'lat' in element:
                        water_lat = element['lat']
                        water_lon = element['lon']
                    else:
                        continue
                    
                    lat_diff = abs(lat - water_lat) * 111
                    lon_diff = abs(lon - water_lon) * 111 * 0.9
                    distance = (lat_diff**2 + lon_diff**2)**0.5
                    
                    min_distance = min(min_distance, distance)
                
                if min_distance < float('inf'):
                    proximity = max(0, min(1, 1 - (min_distance / 10)))
                else:
                    proximity = 0.3
                
                return {
                    'proximity_to_water': float(proximity),
                    'distance_km': float(min_distance) if min_distance < float('inf') else 10.0,
                    'success': True
                }
            else:
                return {
                    'proximity_to_water': 0.2,
                    'distance_km': 10.0,
                    'success': True
                }
        
        except Exception as e:
            return {
                'proximity_to_water': 0.3,
                'distance_km': 5.0,
                'success': False
            }
    
    def get_vegetation_cover(self, lat, lon):
        """Estimate vegetation from location data"""
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                'latitude': lat,
                'longitude': lon,
                'daily': 'et0_fao_evapotranspiration',
                'timezone': 'auto'
            }
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            et_values = data.get('daily', {}).get('et0_fao_evapotranspiration', [3.0])
            avg_et = sum(et_values[:3]) / len(et_values[:3])
            
            vegetation = min(max((avg_et - 1) / 5, 0.2), 0.9)
            
            return {
                'vegetation_cover': float(vegetation),
                'success': True
            }
        
        except Exception as e:
            return {
                'vegetation_cover': 0.5,
                'success': False
            }
    
    def estimate_soil_type(self, lat, lon, elevation):
        """Estimate soil type based on terrain"""
        if elevation > 1500:
            soil = 'Gravel'
        elif elevation > 800:
            soil = 'Silt'
        else:
            soil = 'Sand'
        
        return {
            'soil_type': soil,
            'success': True
        }
    
    def fetch_all_data(self, lat, lon):
        """Fetch all environmental data from FREE APIs"""
        data = {
            'lat': lat,
            'lon': lon,
            'timestamp': datetime.now().isoformat()
        }
        
        weather = self.get_weather_open_meteo(lat, lon)
        data['rainfall_mm'] = weather['rainfall_mm']
        data['soil_saturation'] = weather['soil_saturation']
        data['humidity'] = weather['humidity']
        
        terrain = self.get_elevation_slope(lat, lon)
        data['slope_angle'] = terrain['slope_angle']
        data['elevation'] = terrain['elevation']
        
        earthquake = self.get_earthquake_activity(lat, lon)
        data['earthquake_activity'] = earthquake['earthquake_activity']
        data['earthquake_count'] = earthquake.get('earthquake_count', 0)
        
        water = self.get_water_proximity(lat, lon)
        data['proximity_to_water'] = water['proximity_to_water']
        data['water_distance_km'] = water.get('distance_km', 5.0)
        
        vegetation = self.get_vegetation_cover(lat, lon)
        data['vegetation_cover'] = vegetation['vegetation_cover']
        
        soil = self.estimate_soil_type(lat, lon, data['elevation'])
        data['soil_type'] = soil['soil_type']
        
        return data


def setup_model():
    """Extract model if needed"""
    if not os.path.exists('model_package/prediction_api.py'):
        with zipfile.ZipFile('model_package.zip', 'r') as zip_ref:
            zip_ref.extractall('.')

def predict_with_free_apis(lat, lon):
    """Make landslide prediction using FREE APIs only"""
    setup_model()
    
    sys.path.append('model_package')
    from prediction_api import LandslidePredictor
    
    predictor = LandslidePredictor(model_dir='model_package/models')
    
    fetcher = FreeAPIDataFetcher()
    env_data = fetcher.fetch_all_data(lat, lon)
    
    result = predictor.predict(
        lat=env_data['lat'],
        lon=env_data['lon'],
        rainfall_mm=env_data['rainfall_mm'],
        slope_angle=env_data['slope_angle'],
        soil_saturation=env_data['soil_saturation'],
        vegetation_cover=env_data['vegetation_cover'],
        earthquake_activity=env_data['earthquake_activity'],
        proximity_to_water=env_data['proximity_to_water'],
        soil_type=env_data['soil_type']
    )
    
    return result, env_data


def batch_predict_free_apis(locations_list):
    """Predict for multiple locations using FREE APIs"""
    results = []
    
    print(f"Processing {len(locations_list)} locations in Manipur...\n")
    
    for i, location in enumerate(locations_list, 1):
        if isinstance(location, tuple):
            lat, lon = location
            name = f"Location {i}"
        else:
            lat = location['lat']
            lon = location['lon']
            name = location.get('name', f"Location {i}")
        
        print(f"[{i}/{len(locations_list)}] {name} ({lat:.4f}, {lon:.4f})...", end=" ")
        
        try:
            result, env_data = predict_with_free_apis(lat, lon)
            result['location_name'] = name
            results.append({**result, **env_data})
            
            risk_icon = "🚨" if result['risk_level'] in ['HIGH', 'EXTREME'] else "⚠️" if result['risk_level'] == 'MODERATE' else "✓"
            print(f"{risk_icon} {result['risk_level']} ({result['landslide_probability']:.1%})")
            
            if i < len(locations_list):
                time.sleep(2)
        
        except Exception as e:
            print(f"❌ Error: {str(e)[:50]}")
            continue
    
    results_df = pd.DataFrame(results)
    
    results_df.to_csv('manipur_predictions.csv', index=False)
    print(f"\n{'='*70}")
    print("RESULTS SUMMARY")
    print(f"{'='*70}\n")
    
    print(f"Total Locations Analyzed: {len(results_df)}\n")
    
    print("Risk Level Distribution:")
    risk_counts = results_df['risk_level'].value_counts()
    for risk_level, count in risk_counts.items():
        percentage = (count / len(results_df)) * 100
        print(f"  {risk_level:12s}: {count:3d} ({percentage:5.1f}%)")
    
    alerts = results_df[results_df['risk_level'].isin(['HIGH', 'EXTREME'])]
    if not alerts.empty:
        print(f"\n{'='*70}")
        print(f"⚠️  HIGH-RISK ALERTS: {len(alerts)} LOCATIONS")
        print(f"{'='*70}\n")
        
        for _, row in alerts.iterrows():
            print(f"  📍 {row['location_name']}")
            print(f"     Location: ({row['lat']:.4f}, {row['lon']:.4f})")
            print(f"     Risk: {row['risk_level']} | Probability: {row['landslide_probability']:.1%}")
            print(f"     Rainfall: {row['rainfall_mm']:.1f}mm | Slope: {row['slope_angle']:.1f}°")
            print(f"     Elevation: {row['elevation']:.0f}m | Soil: {row['soil_type']}")
            print()
        
        alerts.to_csv('manipur_alerts.csv', index=False)
        print(f"  ✅ High-risk locations saved to 'manipur_alerts.csv'")
    else:
        print(f"\n✓ No high-risk locations detected")
    
    print(f"\n✅ Full results saved to 'manipur_predictions.csv'")
    print(f"{'='*70}\n")
    
    return results_df


    
   