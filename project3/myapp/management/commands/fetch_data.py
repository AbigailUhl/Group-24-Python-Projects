import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from myapp.models import WeatherRecord

BASE_URL = "https://api.open-meteo.com/v1/forecast"


class Command(BaseCommand):
    help = "Fetch weather data from Open-Meteo"

    def handle(self, *args, **options):
        cities = {
            "Tallahassee": {"latitude": 30.4383, "longitude": -84.2807},
            "Miami": {"latitude": 25.7617, "longitude": -80.1918},
            "Atlanta": {"latitude": 33.7490, "longitude": -84.3880},
        }

        for city_name, coords in cities.items():
            params = {
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                "timezone": "auto",
            }

            max_retries = 2
            data = None

            for attempt in range(max_retries):
                try:
                    response = requests.get(BASE_URL, params=params, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    break

                except requests.exceptions.Timeout:
                    self.stderr.write(
                        self.style.ERROR(
                            f"{city_name}: timeout on attempt {attempt + 1}"
                        )
                    )

                except requests.exceptions.RequestException as e:
                    self.stderr.write(
                        self.style.ERROR(
                            f"{city_name}: error on attempt {attempt + 1} - {e}"
                        )
                    )

            if data is None:
                self.stderr.write(
                    self.style.ERROR(f"{city_name}: failed after {max_retries} attempts")
                )
                continue

            daily = data.get("daily", {})
            dates = daily.get("time", [])
            max_temps = daily.get("temperature_2m_max", [])
            min_temps = daily.get("temperature_2m_min", [])
            precipitation = daily.get("precipitation_sum", [])

            if not dates:
                self.stderr.write(self.style.ERROR(f"{city_name}: no daily data found"))
                continue

            max_days = 7

            for i in range(min(len(dates), max_days)):
                date_obj = datetime.strptime(dates[i], "%Y-%m-%d").date()

                WeatherRecord.objects.update_or_create(
                    city=city_name,
                    date=date_obj,
                    defaults={
                        "temperature_max": max_temps[i] if i < len(max_temps) else None,
                        "temperature_min": min_temps[i] if i < len(min_temps) else None,
                        "precipitation_sum": precipitation[i] if i < len(precipitation) else None,
                    },
                )

            self.stdout.write(self.style.SUCCESS(f"Fetched data for {city_name}"))