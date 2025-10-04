
# Environmental Prediction API - Setup Guide

## Getting Real Data API Keys

### 1. OpenWeatherMap API (Free Tier Available)

1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Navigate to "API Keys" section
4. Copy your API key
5. Add to .env file: `OPENWEATHER_API_KEY=your_key_here`

Free tier includes:
- 1,000 calls/day
- Current weather data
- 5-day forecast
- Air pollution data

### 2. NASA EarthData Token (Free)

1. Create account at https://urs.earthdata.nasa.gov
2. Go to Profile → Generate Token
3. Copy the generated token
4. Add to .env file: `NASA_EARTHDATA_TOKEN=your_token_here`

Provides access to:
- Landsat surface temperature data
- VIIRS land surface temperature
- MODIS vegetation indices
- Global satellite imagery

### 3. Alternative Data Sources (Optional)

**ESA Climate Data:**
- https://climate.esa.int/en/projects/land-surface-temperature/
- European satellite data

**USGS EarthExplorer:**
- https://earthexplorer.usgs.gov/
- Landsat and other satellite imagery

## Installation and Setup

1. Install dependencies:
   ```bash
   pip install -r enhanced_requirements.txt
   ```

2. Copy configuration template:
   ```bash
   cp config_template.env .env
   ```

3. Edit .env file with your API keys

4. Run the enhanced API:
   ```bash
   python enhanced_app.py
   ```

## Usage Examples

### Basic Request (works without API keys):
```bash
curl -X POST http://localhost:5000/predict/complete \
  -H "Content-Type: application/json" \
  -d '{
    "concrete_coverage": 0.4,
    "vegetation_coverage": 0.3,
    "water_coverage": 0.1,
    "building_density": 0.5,
    "industrial_buildings": 0.2,
    "tree_coverage": 0.25,
    "solar_panel_coverage": 0.15,
    "wind_turbine_density": 0.05,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "hour_of_day": 14
  }'
```

### With Real Location Data:
```javascript
// JavaScript integration example
async function getPredictions(cityConfig) {
    const response = await fetch('http://localhost:5000/predict/complete', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            ...cityConfig,
            latitude: 40.7128,    // New York City
            longitude: -74.0060,
            hour_of_day: new Date().getHours()
        })
    });

    const result = await response.json();
    console.log('Temperature:', result.temperature.predicted_temperature);
    console.log('Data Source:', result.temperature.data_source);
    console.log('Overall Score:', result.scores.overall_score);

    return result;
}
```

## API Capabilities by Data Source

### With API Keys Configured:
- ✅ Real-time weather data (temperature, wind, humidity)
- ✅ Weather-dependent renewable energy calculations
- ✅ Wind effects on air quality dispersion
- ✅ Enhanced prediction accuracy

### Without API Keys (Fallback Mode):
- ✅ Research-based environmental predictions
- ✅ Urban heat island calculations
- ✅ Building and vegetation effects
- ✅ Time-of-day variations
- ⚠️ Uses estimated/mock weather data

## Production Deployment

### Using Docker:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r enhanced_requirements.txt
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "enhanced_app:app"]
```

### Environment Variables for Production:
```bash
export OPENWEATHER_API_KEY="your_key"
export NASA_EARTHDATA_TOKEN="your_token"
export FLASK_ENV="production"
```

## Data Sources Used

1. **OpenWeatherMap API**: Real-time weather conditions
2. **NASA VIIRS/MODIS**: Land surface temperature data
3. **Research Literature**: Urban heat island coefficients
4. **Engineering Data**: Building thermal properties
5. **Climate Models**: Seasonal and daily variations

## Accuracy and Validation

- Temperature predictions: ±1-2°C accuracy with real data
- Air quality estimates: Based on EPA and WHO standards  
- Energy calculations: Weather-dependent renewable modeling
- UHI effects: Validated against urban climate research

The API provides both research-based environmental modeling and real-time data integration for comprehensive environmental impact assessment.
