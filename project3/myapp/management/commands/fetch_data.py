import requests

from django.core.management.base import BaseCommand
from myapp.models import WeatherRecord


class Command(BaseCommand):
    help = "Fetch weather data from Open-Meteo"

    def handle(self, *args, **options):
        cities = {
            "Tallahassee": {"latitude": 30.4383, "longitude": -84.2807},
            "Miami": {"latitude": 25.7617, "longitude": -80.1918},
            "Atlanta": {"latitude": 33.7490, "longitude": -84.3880},
        }

        for city_name, coords in cities.items():
            try:
                response = requests.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": coords["latitude"],
                        "longitude": coords["longitude"],
                        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                        "timezone": "auto",
                    },
                    timeout=10,
                )
                response.raise_for_status()
                data = response.json()

                dates = data["daily"]["time"]
                max_temps = data["daily"]["temperature_2m_max"]
                min_temps = data["daily"]["temperature_2m_min"]
                precipitation = data["daily"]["precipitation_sum"]

                for i in range(len(dates)):
                    WeatherRecord.objects.update_or_create(
                        city=city_name,
                        date=dates[i],
                        defaults={
                            "temperature_max": max_temps[i],
                            "temperature_min": min_temps[i],
                            "precipitation_sum": precipitation[i],
                        },
                    )

                self.stdout.write(self.style.SUCCESS(f"Fetched data for {city_name}"))

            except requests.exceptions.RequestException as e:
                self.stderr.write(self.style.ERROR(f"Error fetching data for {city_name}: {e}"))