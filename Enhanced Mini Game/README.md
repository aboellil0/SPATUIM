
# Environmental Prediction API - Deployment Instructions

## Files Created:
1. app.py - Main Flask API application
2. requirements.txt - Python dependencies 
3. test_api.py - API testing script
4. environmental_training_data.csv - Training dataset (10,000 samples)

## Local Development Setup:

1. Install dependencies:
   pip install -r requirements.txt

2. Run the API:
   python app.py

3. Test the API:
   python test_api.py

## API Endpoints:

- GET /health - Health check
- POST /predict/temperature - Temperature prediction
- POST /predict/air_quality - Air quality prediction
- POST /predict/energy - Energy balance prediction  
- POST /predict/complete - Complete environmental assessment
- GET /api/docs - API documentation

## Sample Request:
POST /predict/complete
Content-Type: application/json

{
    "concrete_coverage": 0.4,
    "vegetation_coverage": 0.3,
    "water_coverage": 0.1,
    "building_density": 0.5,
    "industrial_buildings": 0.2,
    "tree_coverage": 0.25,
    "base_temperature": 22.0,
    "hour_of_day": 14,
    "wind_speed": 5.0,
    "solar_panel_coverage": 0.15,
    "wind_turbine_density": 0.05
}

## Production Deployment:

1. Using Gunicorn:
   gunicorn --bind 0.0.0.0:5000 app:app

2. Using Docker:
   - Create Dockerfile
   - Build and run container

3. Cloud deployment options:
   - Heroku
   - AWS Lambda
   - Google Cloud Run
   - Digital Ocean App Platform

## Integration with Your Game:

Your game can send HTTP POST requests to the API with city configuration data and receive environmental predictions in real-time.

Example JavaScript integration:
```javascript
async function getPredictions(cityConfig) {
    const response = await fetch('http://localhost:5000/predict/complete', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(cityConfig)
    });
    return await response.json();
}
```
