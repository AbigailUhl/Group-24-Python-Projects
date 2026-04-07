import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_URL = "https://api.open-meteo.com/v1/forecast"

CITIES = {
    "Tallahassee": {"latitude": 30.4383, "longitude": -84.2807},
    "Miami": {"latitude": 25.7617, "longitude": -80.1918},
    "Atlanta": {"latitude": 33.7490, "longitude": -84.3880}
}

OUTPUT_FILE = Path("data/processed/weather_data.csv")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

def fetch_weather_data(city, coords):
    params = {
            "latitude": coords["latitude"],
            "longitude": coords["longitude"],
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
            "timezone": "auto"
    }
    results = []
    max_retries = 2
    data = None

    for attempt in range(max_retries):
        try:
            response = requests.get(BASE_URL, params=params, timeout=10)
            print(f"{city}: {response.status_code}")

            response.raise_for_status()
            data = response.json()
            break  # success → exit loop

        except requests.exceptions.Timeout:
            print(f"{city}: timeout on attempt {attempt + 1}")

        except requests.exceptions.RequestException as e:
            print(f"{city}: error on attempt {attempt + 1} → {e}")

    if data is None:
        print(f"{city}: failed after {max_retries} attempts")
        return []
     
    daily = data["daily"]
    if not daily:
        print(f"No daily data for {city}")
        return []

    run_timestamp = datetime.now().isoformat()
    for i in range(len(daily["time"])):
        row = {
            "run_timestamp": run_timestamp,
            "city": city,
            "date": daily["time"][i],
            "temperature_max": daily["temperature_2m_max"][i],
            "temperature_min": daily["temperature_2m_min"][i],
            "precipitation_sum": daily["precipitation_sum"][i],
            "wind_speed_max": daily["wind_speed_10m_max"][i]
        }
        results.append(row)

    return results

def save_to_csv(df, output_file):
    if df.empty:
        return

    if output_file.exists():
        df.to_csv(output_file, mode="a", header=False, index=False)
    else:
        df.to_csv(output_file, index=False)

def main():
    all_results = []

    for city, coords in CITIES.items():
        all_results.extend(fetch_weather_data(city, coords))

    df = pd.DataFrame(all_results)
    save_to_csv(df, OUTPUT_FILE)

if __name__ == "__main__":
    main()