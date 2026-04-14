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

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "data/processed/weather_data.csv"
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

            if response.status_code == 200:
                data = response.json()
                break
            else:
                print(f"{city}: request failed with status {response.status_code}")
                response.raise_for_status()

        except requests.exceptions.Timeout:
            print(f"{city}: timeout on attempt {attempt + 1}")

        except requests.exceptions.RequestException as e:
            print(f"{city}: error on attempt {attempt + 1} → {e}")

    if data is None:
        print(f"{city}: failed after {max_retries} attempts")
        return []
    
    daily = data.get("daily", {})
    times = daily.get("time", [])
    temp_max = daily.get("temperature_2m_max", [])
    temp_min = daily.get("temperature_2m_min", [])
    precipitation = daily.get("precipitation_sum", [])
    wind_speed = daily.get("wind_speed_10m_max", [])
     
    if not times:
        print(f"{city}: no daily data found")
        return []

    run_timestamp = datetime.now().isoformat()

    max_days = 7
    for i in range(min(len(times), max_days)):
        row = {
            "run_timestamp": run_timestamp,
            "city": city,
            "date": times[i],
            "temperature_max": temp_max[i] if i < len(temp_max) else None,
            "temperature_min": temp_min[i] if i < len(temp_min) else None,
            "precipitation_sum": precipitation[i] if i < len(precipitation) else None,
            "wind_speed_max": wind_speed[i] if i < len(wind_speed) else None
        }
        results.append(row)
    return results

def save_to_csv(df, output_file):
    if df.empty:
        print("No data to save.")
        return

    if output_file.exists():
        df.to_csv(output_file, mode="a", header=False, index=False)
        print(f"Appended {len(df)} rows to {output_file}")
    else:
        df.to_csv(output_file, index=False)
        print(f"Created {output_file} with {len(df)} rows")

def main():
    all_results = []

    for city, coords in CITIES.items():
        all_results.extend(fetch_weather_data(city, coords))

    df = pd.DataFrame(all_results)
    save_to_csv(df, OUTPUT_FILE)

if __name__ == "__main__":
    main()