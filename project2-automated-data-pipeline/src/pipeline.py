import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_URL = "https://api.open-meteo.com/v1/forecast"

cities = {
    "Tallahassee": {"latitude": 30.4383, "longitude": -84.2807},
    "Miami": {"latitude": 25.7617, "longitude": -80.1918},
    "Atlanta": {"latitude": 33.7490, "longitude": -84.3880}
}
all_results = []

for city, coords in cities.items():
    params = {
        "latitude": coords["latitude"],
        "longitude": coords["longitude"],
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
        "timezone": "auto"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()  # raises error if status is not 200

        data = response.json()
        daily = data["daily"]

        for i in range(len(daily["time"])):
            row = {
                "city": city,
                "date": daily["time"][i],
                "temperature_max": daily["temperature_2m_max"][i],
                "temperature_min": daily["temperature_2m_min"][i],
                "precipitation_sum": daily["precipitation_sum"][i],
                "wind_speed_max": daily["wind_speed_10m_max"][i]
            }
            all_results.append(row)

    except requests.exceptions.Timeout:
        print(f"Request timed out for {city}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed for {city}: {e}")

df = pd.DataFrame(all_results)
OUTPUT_FILE = Path("data/processed/weather_data.csv")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

if OUTPUT_FILE.exists():
    df.to_csv(OUTPUT_FILE, mode="a", header=False, index=False)
else:
    df.to_csv(OUTPUT_FILE, index=False)