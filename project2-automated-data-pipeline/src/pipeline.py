import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 30.4383,
    "longitude": -84.2807,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
    "timezone": "auto"
}

response = requests.get(BASE_URL, params=params, timeout=10)

print("Status code:", response.status_code)

data = response.json()
print(data)