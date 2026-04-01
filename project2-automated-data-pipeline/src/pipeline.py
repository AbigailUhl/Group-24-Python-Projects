import requests

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

    response = requests.get(BASE_URL, params=params, timeout=10)
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

for row in all_results:
    print(row)