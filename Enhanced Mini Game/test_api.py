
import requests
import json

# Test the API
base_url = "http://localhost:5000"

# Test data
test_city = {
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

def test_api():
    # Test health endpoint
    response = requests.get(f"{base_url}/health")
    print("Health check:", response.json())

    # Test complete prediction
    response = requests.post(f"{base_url}/predict/complete", json=test_city)
    result = response.json()

    print("\nComplete Environmental Assessment:")
    print(f"Temperature: {result['temperature']['predicted_temperature']}°C")
    print(f"Air Quality Index: {result['air_quality']['air_quality_index']}")
    print(f"Energy Balance: {result['energy']['energy_balance']} kWh")
    print(f"Overall Score: {result['overall_score']}/100")
    print(f"Recommendations: {result['recommendations']}")

if __name__ == "__main__":
    test_api()
