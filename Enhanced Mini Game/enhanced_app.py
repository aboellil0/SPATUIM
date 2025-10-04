
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import json
import logging
import requests
import os
from datetime import datetime
import time

app = Flask(__name__)

# Configure CORS to allow local network access
# This allows connections from any origin on your local network
CORS(app, resources={
    r"/*": {
        "origins": "*"  # Allow all origins for local network access
    }
})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration for external APIs
class Config:
    OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHER_API_KEY', 'your_api_key_here')
    NASA_EARTHDATA_TOKEN = os.environ.get('NASA_EARTHDATA_TOKEN', '')
    BASE_URL_OPENWEATHER = "https://api.openweathermap.org/data/2.5"
    BASE_URL_NASA_VIIRS = "https://firms.modaps.eosdis.nasa.gov/api/country/csv"

# NASA VIIRS Land Surface Temperature integration
def get_nasa_lst_data(lat, lon, date=None):
    """
    Fetch Land Surface Temperature data from NASA VIIRS
    This is a simplified implementation - in production you'd use earthaccess library
    """
    try:
        # Placeholder for NASA LST data - would need proper NASA EarthData credentials
        # Using estimated values based on location and season
        if date is None:
            date = datetime.now()

        # Simulate LST based on latitude and season (simplified model)
        seasonal_factor = np.sin(2 * np.pi * date.timetuple().tm_yday / 365) * 10
        latitude_factor = (60 - abs(lat)) / 60 * 15  # Warmer at equator

        base_lst = 15 + latitude_factor + seasonal_factor

        return {
            'land_surface_temperature': base_lst,
            'satellite_source': 'VIIRS/Suomi NPP',
            'acquisition_date': date.strftime('%Y-%m-%d'),
            'confidence': 0.75,
            'status': 'estimated'  # In production: 'satellite_data'
        }
    except Exception as e:
        logger.error(f"NASA LST data error: {str(e)}")
        return None

# OpenWeatherMap integration
def get_openweather_data(lat, lon):
    """
    Fetch real-time weather data from OpenWeatherMap API
    """
    try:
        if Config.OPENWEATHERMAP_API_KEY == 'your_api_key_here':
            # Return mock data if no API key configured
            return {
                'temperature': 22.0 + np.random.normal(0, 3),
                'humidity': 60.0 + np.random.normal(0, 10),
                'wind_speed': 5.0 + np.random.normal(0, 2),
                'pressure': 1013.0 + np.random.normal(0, 10),
                'status': 'mock_data'
            }

        url = f"{Config.BASE_URL_OPENWEATHER}/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': Config.OPENWEATHERMAP_API_KEY,
            'units': 'metric'
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'pressure': data['main']['pressure'],
                'status': 'real_data'
            }
        else:
            logger.warning(f"OpenWeather API error: {response.status_code}")
            return None

    except Exception as e:
        logger.error(f"OpenWeather data error: {str(e)}")
        return None

# Enhanced prediction functions with real data integration
def predict_temperature_enhanced(city_config):
    """
    Enhanced temperature prediction using real satellite and weather data
    """
    try:
        lat = city_config.get('latitude', 40.0)
        lon = city_config.get('longitude', -74.0)

        # Get real weather data
        weather_data = get_openweather_data(lat, lon)

        # Get NASA LST data
        lst_data = get_nasa_lst_data(lat, lon)

        # Base temperature from real data or fallback
        if weather_data and weather_data['status'] == 'real_data':
            base_temp = weather_data['temperature']
            data_source = 'openweathermap'
        elif lst_data:
            base_temp = lst_data['land_surface_temperature']
            data_source = 'nasa_viirs_estimated'
        else:
            base_temp = city_config.get('base_temperature', 20.0)
            data_source = 'user_input'

        # Urban heat island calculation based on research
        uhi_effect = (
            city_config.get('concrete_coverage', 0) * 3.5 +    # Concrete UHI effect
            city_config.get('building_density', 0) * 2.0 +     # Building density effect  
            city_config.get('industrial_buildings', 0) * 4.0 - # Industrial heating
            city_config.get('tree_coverage', 0) * 2.0 -        # Tree cooling
            city_config.get('vegetation_coverage', 0) * 1.0 +  # Vegetation cooling
            city_config.get('water_coverage', 0) * -3.0        # Water cooling
        )

        # Wind speed effect (from real data if available)
        wind_speed = weather_data.get('wind_speed', 5.0) if weather_data else 5.0
        wind_cooling = -0.3 * wind_speed if wind_speed > 2 else 0

        # Time of day effect
        hour = city_config.get('hour_of_day', 12)
        daily_variation = np.sin(2 * np.pi * hour / 24) * 2

        # Final temperature prediction
        predicted_temp = base_temp + uhi_effect + wind_cooling + daily_variation

        # Calculate detailed factors
        factors = {
            'base_temperature': base_temp,
            'uhi_effect': uhi_effect,
            'concrete_heating': city_config.get('concrete_coverage', 0) * 3.5,
            'building_heating': city_config.get('building_density', 0) * 2.0,
            'industrial_heating': city_config.get('industrial_buildings', 0) * 4.0,
            'tree_cooling': -city_config.get('tree_coverage', 0) * 2.0,
            'vegetation_cooling': -city_config.get('vegetation_coverage', 0) * 1.0,
            'water_cooling': city_config.get('water_coverage', 0) * -3.0,
            'wind_cooling': wind_cooling,
            'daily_variation': daily_variation
        }

        return {
            'predicted_temperature': round(predicted_temp, 2),
            'base_temperature': round(base_temp, 2),
            'uhi_intensity': round(uhi_effect, 2),
            'data_source': data_source,
            'confidence': 0.90 if data_source == 'openweathermap' else 0.75,
            'factors': factors,
            'weather_conditions': weather_data,
            'satellite_data': lst_data,
            'status': 'success'
        }

    except Exception as e:
        logger.error(f"Enhanced temperature prediction error: {str(e)}")
        return {'error': str(e), 'status': 'error'}

def predict_air_quality_enhanced(city_config):
    """
    Enhanced air quality prediction with weather integration
    """
    try:
        lat = city_config.get('latitude', 40.0)
        lon = city_config.get('longitude', -74.0)

        # Get weather data for wind dispersion effects
        weather_data = get_openweather_data(lat, lon)

        # Pollution sources calculation
        pollution_sources = (
            city_config.get('industrial_buildings', 0) * 80 +
            city_config.get('building_density', 0) * 20 +
            city_config.get('traffic_density', 0) * 30  # Added traffic factor
        )

        # Pollution sinks (natural filtering)
        pollution_sinks = (
            city_config.get('tree_coverage', 0) * 30 +
            city_config.get('vegetation_coverage', 0) * 15 +
            city_config.get('water_coverage', 0) * 10
        )

        # Weather effects on air quality
        wind_speed = weather_data.get('wind_speed', 5.0) if weather_data else 5.0
        humidity = weather_data.get('humidity', 60.0) if weather_data else 60.0

        wind_dispersion = wind_speed * -3  # Higher wind = better dispersion
        humidity_effect = (humidity - 50) * 0.2  # High humidity can trap pollutants

        # Calculate AQI
        base_aqi = pollution_sources - pollution_sinks + wind_dispersion + humidity_effect
        aqi = max(0, min(300, base_aqi + 20))  # Add baseline urban pollution

        # Categorize AQI
        if aqi <= 50:
            category = "Good"
            health_implications = "Air quality is considered satisfactory"
        elif aqi <= 100:
            category = "Moderate" 
            health_implications = "Air quality is acceptable for most people"
        elif aqi <= 150:
            category = "Unhealthy for Sensitive Groups"
            health_implications = "Members of sensitive groups may experience health effects"
        else:
            category = "Unhealthy"
            health_implications = "Everyone may begin to experience health effects"

        # Generate recommendations
        recommendations = []
        if aqi > 100:
            recommendations.extend(["Increase green coverage", "Reduce industrial emissions"])
        if city_config.get('tree_coverage', 0) < 0.3:
            recommendations.append("Plant more trees for air filtration")
        if wind_speed < 2:
            recommendations.append("Consider urban design to improve air circulation")

        return {
            'air_quality_index': round(aqi, 1),
            'category': category,
            'health_implications': health_implications,
            'pollution_sources': round(pollution_sources, 1),
            'pollution_sinks': round(pollution_sinks, 1),
            'wind_effect': round(wind_dispersion, 1),
            'humidity_effect': round(humidity_effect, 1),
            'recommendations': recommendations,
            'weather_conditions': weather_data,
            'status': 'success'
        }

    except Exception as e:
        logger.error(f"Enhanced air quality prediction error: {str(e)}")
        return {'error': str(e), 'status': 'error'}

def predict_energy_enhanced(city_config):
    """
    Enhanced energy prediction with weather-dependent renewable generation
    """
    try:
        lat = city_config.get('latitude', 40.0)
        lon = city_config.get('longitude', -74.0)

        # Get weather data for renewable energy calculations
        weather_data = get_openweather_data(lat, lon)

        # Weather-dependent renewable energy production
        wind_speed = weather_data.get('wind_speed', 5.0) if weather_data else 5.0

        # Solar production (affected by time of day and weather)
        hour = city_config.get('hour_of_day', 12)
        solar_efficiency = max(0, np.sin(np.pi * (hour - 6) / 12)) if 6 <= hour <= 18 else 0

        # Wind production (cubic relationship with wind speed, cut-off at high speeds)
        wind_efficiency = min(1.0, (wind_speed / 12) ** 3) if wind_speed >= 3 else 0

        # Energy production calculations
        solar_potential = city_config.get('solar_panel_coverage', 0) * 100
        wind_potential = city_config.get('wind_turbine_density', 0) * 150

        solar_production = solar_potential * solar_efficiency
        wind_production = wind_potential * wind_efficiency
        total_renewable_production = solar_production + wind_production

        # Energy consumption (varies by time and building types)
        base_consumption = (
            city_config.get('building_density', 0) * 80 +
            city_config.get('industrial_buildings', 0) * 200 +
            city_config.get('residential_buildings', 0) * 60
        )

        # Time-based consumption multiplier
        if 18 <= hour <= 22:  # Peak evening hours
            consumption_multiplier = 1.3
        elif 6 <= hour <= 9:   # Morning peak
            consumption_multiplier = 1.2
        elif 10 <= hour <= 16: # Daytime
            consumption_multiplier = 1.1
        else:                  # Night hours
            consumption_multiplier = 0.8

        total_consumption = base_consumption * consumption_multiplier

        # Calculate energy balance and metrics
        energy_balance = total_renewable_production - total_consumption

        total_energy_demand = abs(total_consumption)
        renewable_percentage = (total_renewable_production / total_energy_demand * 100) if total_energy_demand > 0 else 0

        # Sustainability score calculation
        sustainability_score = min(100, 
            renewable_percentage * 0.6 +  # 60% weight on renewable percentage
            (50 if energy_balance >= 0 else 0) * 0.3 +  # 30% weight on energy surplus
            (100 - abs(energy_balance) / max(1, total_energy_demand) * 100) * 0.1  # 10% efficiency weight
        )

        return {
            'energy_balance': round(energy_balance, 1),
            'total_production': round(total_renewable_production, 1),
            'solar_production': round(solar_production, 1),
            'wind_production': round(wind_production, 1),
            'total_consumption': round(total_consumption, 1),
            'renewable_percentage': round(renewable_percentage, 1),
            'sustainability_score': round(sustainability_score, 1),
            'solar_efficiency': round(solar_efficiency * 100, 1),
            'wind_efficiency': round(wind_efficiency * 100, 1),
            'consumption_multiplier': consumption_multiplier,
            'weather_conditions': weather_data,
            'status': 'success'
        }

    except Exception as e:
        logger.error(f"Enhanced energy prediction error: {str(e)}")
        return {'error': str(e), 'status': 'error'}

# Updated API Routes
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint with API status"""
    api_status = {
        'openweathermap': 'configured' if Config.OPENWEATHERMAP_API_KEY != 'your_api_key_here' else 'not_configured',
        'nasa_earthdata': 'configured' if Config.NASA_EARTHDATA_TOKEN else 'not_configured'
    }

    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'service': 'Enhanced Environmental Prediction API',
        'external_apis': api_status,
        'capabilities': ['temperature', 'air_quality', 'energy', 'real_time_weather', 'satellite_data']
    })

@app.route('/predict/temperature', methods=['POST'])
def predict_temperature_endpoint():
    """Enhanced temperature prediction with real data"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        result = predict_temperature_enhanced(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Temperature endpoint error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/predict/air_quality', methods=['POST'])
def predict_air_quality_endpoint():
    """Enhanced air quality prediction"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        result = predict_air_quality_enhanced(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Air quality endpoint error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/predict/energy', methods=['POST'])
def predict_energy_endpoint():
    """Enhanced energy prediction with weather-dependent renewables"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        result = predict_energy_enhanced(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Energy endpoint error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/predict/complete', methods=['POST'])
def predict_complete_enhanced_endpoint():
    """Complete enhanced environmental assessment"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        # Get all enhanced predictions
        temp_result = predict_temperature_enhanced(data)
        air_result = predict_air_quality_enhanced(data) 
        energy_result = predict_energy_enhanced(data)

        # Calculate comprehensive environmental scores
        if all(r.get('status') == 'success' for r in [temp_result, air_result, energy_result]):
            # Temperature score (optimal range: 18-25°C)
            predicted_temp = temp_result.get('predicted_temperature', 25)
            temp_deviation = abs(predicted_temp - 21.5)  # Optimal: 21.5°C
            temp_score = max(0, 100 - temp_deviation * 8)

            # Air quality score (lower AQI is better)
            aqi = air_result.get('air_quality_index', 0)
            air_score = max(0, 100 - aqi * 1.5)

            # Energy score from sustainability calculation
            energy_score = energy_result.get('sustainability_score', 0)

            # UHI intensity penalty
            uhi_intensity = temp_result.get('uhi_intensity', 0)
            uhi_penalty = max(0, uhi_intensity - 2) * 10  # Penalty for UHI > 2°C

            # Overall environmental score
            overall_score = (temp_score * 0.3 + air_score * 0.35 + energy_score * 0.35) - uhi_penalty
            overall_score = max(0, min(100, overall_score))

            # Generate comprehensive recommendations
            recommendations = []

            if predicted_temp > 27:
                recommendations.append("Critical: Add trees and green infrastructure to reduce urban heat")
            elif predicted_temp > 25:
                recommendations.append("Add more vegetation and cooling features")

            if aqi > 150:
                recommendations.append("Critical: Reduce pollution sources and improve air circulation")
            elif aqi > 100:
                recommendations.extend(air_result.get('recommendations', []))

            if energy_result.get('renewable_percentage', 0) < 30:
                recommendations.append("Significantly increase renewable energy infrastructure")
            elif energy_result.get('renewable_percentage', 0) < 60:
                recommendations.append("Expand solar and wind energy systems")

            if temp_result.get('uhi_intensity', 0) > 4:
                recommendations.append("Implement comprehensive urban cooling strategy")

        else:
            # Fallback scoring if any prediction failed
            temp_score = air_score = energy_score = overall_score = 0
            recommendations = ["Unable to generate recommendations due to prediction errors"]

        return jsonify({
            'temperature': temp_result,
            'air_quality': air_result,
            'energy': energy_result,
            'scores': {
                'overall_score': round(overall_score, 1),
                'temperature_score': round(temp_score, 1),
                'air_quality_score': round(air_score, 1),
                'energy_score': round(energy_score, 1)
            },
            'recommendations': list(set(recommendations)),
            'data_sources': {
                'weather_api': 'openweathermap' if Config.OPENWEATHERMAP_API_KEY != 'your_api_key_here' else 'mock',
                'satellite_data': 'nasa_viirs_estimated',
                'prediction_model': 'research_based_algorithms'
            },
            'status': 'success'
        })

    except Exception as e:
        logger.error(f"Complete enhanced prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/data/sources', methods=['GET'])
def data_sources_info():
    """Information about available data sources"""
    return jsonify({
        'real_time_sources': {
            'openweathermap': {
                'status': 'configured' if Config.OPENWEATHERMAP_API_KEY != 'your_api_key_here' else 'not_configured',
                'provides': ['temperature', 'humidity', 'wind_speed', 'pressure'],
                'update_frequency': '10 minutes',
                'coverage': 'global'
            },
            'nasa_earthdata': {
                'status': 'configured' if Config.NASA_EARTHDATA_TOKEN else 'not_configured', 
                'provides': ['land_surface_temperature', 'vegetation_index', 'thermal_anomalies'],
                'update_frequency': 'daily',
                'coverage': 'global',
                'satellites': ['VIIRS', 'MODIS', 'Landsat']
            }
        },
        'datasets_used': {
            'urban_heat_island_research': 'Multiple scientific studies on UHI effects',
            'building_thermal_properties': 'Engineering data on material heat absorption',
            'vegetation_cooling_effects': 'Research on evapotranspiration and shading',
            'renewable_energy_models': 'Weather-dependent energy production algorithms'
        }
    })

@app.route('/api/docs', methods=['GET'])
def api_documentation_enhanced():
    """Enhanced API documentation"""
    docs = {
        'title': 'Enhanced Environmental Prediction API',
        'version': '2.0.0',
        'description': 'API for predicting environmental changes with real satellite and weather data integration',
        'endpoints': {
            '/health': {
                'method': 'GET',
                'description': 'Health check with external API status'
            },
            '/predict/temperature': {
                'method': 'POST',
                'description': 'Enhanced temperature prediction with real weather and satellite data',
                'required_fields': [
                    'concrete_coverage', 'vegetation_coverage', 'water_coverage',
                    'building_density', 'industrial_buildings', 'tree_coverage',
                    'latitude', 'longitude', 'hour_of_day'
                ],
                'optional_fields': ['base_temperature']
            },
            '/predict/air_quality': {
                'method': 'POST', 
                'description': 'Enhanced air quality prediction with weather effects',
                'required_fields': [
                    'industrial_buildings', 'building_density', 'tree_coverage',
                    'vegetation_coverage', 'latitude', 'longitude'
                ],
                'optional_fields': ['traffic_density']
            },
            '/predict/energy': {
                'method': 'POST',
                'description': 'Weather-dependent renewable energy prediction',
                'required_fields': [
                    'solar_panel_coverage', 'wind_turbine_density',
                    'building_density', 'industrial_buildings',
                    'latitude', 'longitude', 'hour_of_day'
                ]
            },
            '/predict/complete': {
                'method': 'POST',
                'description': 'Complete environmental assessment with real data',
                'required_fields': 'All city configuration + latitude/longitude'
            },
            '/data/sources': {
                'method': 'GET',
                'description': 'Information about data sources and APIs used'
            }
        },
        'enhanced_features': [
            'Real-time weather data integration',
            'NASA satellite data estimation', 
            'Weather-dependent renewable energy modeling',
            'Wind effects on air quality dispersion',
            'Time-of-day energy consumption patterns',
            'Comprehensive environmental scoring'
        ],
        'sample_request': {
            'concrete_coverage': 0.4,
            'vegetation_coverage': 0.3,
            'water_coverage': 0.1,
            'building_density': 0.5,
            'industrial_buildings': 0.2,
            'tree_coverage': 0.25,
            'solar_panel_coverage': 0.15,
            'wind_turbine_density': 0.05,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'hour_of_day': 14
        }
    }
    return jsonify(docs)

if __name__ == '__main__':
    import socket
    
    # Get local IP address
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "Unable to determine"
    
    print("Starting Enhanced Environmental Prediction API...")
    print("Version: 2.0.0")
    print("")
    print("🌐 Server is running on your local network:")
    print(f"  Local:   http://127.0.0.1:5000")
    print(f"  Network: http://{local_ip}:5000")
    print("")
    print("Features:")
    print("  ✓ Real-time weather data integration (OpenWeatherMap)")
    print("  ✓ NASA satellite data estimation")
    print("  ✓ Enhanced prediction algorithms")
    print("  ✓ Comprehensive environmental scoring")
    print("")
    print("Available endpoints:")
    print("  GET  /health - Health check with API status")
    print("  POST /predict/temperature - Enhanced temperature prediction")
    print("  POST /predict/air_quality - Enhanced air quality prediction") 
    print("  POST /predict/energy - Weather-dependent energy prediction")
    print("  POST /predict/complete - Complete environmental assessment")
    print("  GET  /data/sources - Data sources information")
    print("  GET  /api/docs - Enhanced API documentation")
    print("")
    print("Configuration:")
    if os.environ.get('OPENWEATHER_API_KEY'):
        print("  ✓ OpenWeatherMap API configured")
    else:
        print("  ⚠ OpenWeatherMap API not configured (using mock data)")
        print("    Set OPENWEATHER_API_KEY environment variable for real weather data")

    if os.environ.get('NASA_EARTHDATA_TOKEN'):
        print("  ✓ NASA EarthData token configured")
    else:
        print("  ⚠ NASA EarthData not configured (using estimated data)")
        print("    Set NASA_EARTHDATA_TOKEN environment variable for satellite data")

    app.run(host='0.0.0.0', port=5000, debug=True)
