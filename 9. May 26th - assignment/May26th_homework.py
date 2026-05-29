# In Terminal, I need to do > cd ..\Lesson8  > pip install requests > pip freeze


import requests
from datetime import datetime, timedelta
import json
import os

CACHE_FILE = "weather_cache.json"


class WeatherForecast:

    def __init__(self):
        if os.path.exists(CACHE_FILE):
            file = open(CACHE_FILE, "r")
            self._data = json.load(file)
            file.close()
        else:
            self._data = {}

    def _save(self):
        file = open(CACHE_FILE, "w")
        json.dump(self._data, file)
        file.close()

    def __setitem__(self, key, value):
        self._data[key] = value
        self._save()

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def items(self):
        for key in self._data:
            yield (key, self._data[key])


# Main program
print("=" * 40)
print("  Weather Rain Checker")
print("=" * 40)

weather_forecast = WeatherForecast()

while True:
    date_input = input("Enter a date (YYYY-mm-dd) or press Enter for tomorrow: ").strip()

    if date_input == "":
        tomorrow = datetime.now() + timedelta(days=1)
        searched_date = tomorrow.strftime("%Y-%m-%d")
        print("Using tomorrow: " + searched_date)
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            searched_date = date_input
        except ValueError:
            print("Wrong format! Try again.")
            continue

    city = input("Enter a city name (e.g. Cork): ").strip()

    if city == "":
        print("No city entered. Try again.")
        continue

    geo_url = "https://geocoding-api.open-meteo.com/v1/search?name=" + city + "&count=1"

    try:
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if "results" not in geo_data:
            print("City not found. Try again.")
            continue

        latitude = str(geo_data["results"][0]["latitude"])
        longitude = str(geo_data["results"][0]["longitude"])
        city_name = geo_data["results"][0]["name"]
        country = geo_data["results"][0]["country"]
        print("Found: " + city_name + ", " + country)
        print("Latitude: " + latitude + ", Longitude: " + longitude)

    except Exception:
        print("Error finding city. Try again.")
        continue

    # Check cache using WeatherForecast object
    cache_key = latitude + "_" + longitude + "_" + searched_date

    found_in_cache = False
    for key in weather_forecast:
        if key == cache_key:
            found_in_cache = True
            break

    if found_in_cache:
        print("")
        print("[Loaded from cache - no API call needed]")
        precipitation = weather_forecast[cache_key]
    else:
        url = (
            "https://api.open-meteo.com/v1/forecast?"
            "latitude=" + latitude + "&longitude=" + longitude +
            "&daily=precipitation_sum&timezone=Europe%2FLondon"
            "&start_date=" + searched_date + "&end_date=" + searched_date
        )

        try:
            response = requests.get(url)
            data = response.json()
            precipitation = data["daily"]["precipitation_sum"][0]
        except Exception:
            print("Error getting weather data.")
            precipitation = None

        # Save to cache using __setitem__
        weather_forecast[cache_key] = precipitation

    # Show result
    result = "It will rain" if precipitation is not None and precipitation > 0.0 else "It will not rain" if precipitation is not None and precipitation == 0.0 else "I don't know"

    print("")
    print("Date: " + searched_date)
    print("City: " + city_name + ", " + country)
    print("Result: " + result)

    if precipitation is not None and precipitation > 0.0:
        print("Precipitation: " + str(precipitation) + " mm")

    # Show all cached results using items()
    print("")
    print("--- All cached forecasts ---")
    for key, value in weather_forecast.items():
        print("  " + key + " -> " + str(value) + " mm")

    print("")
    again = input("Check another? (yes/no): ").strip().lower()
    if again != "yes" and again != "y":
        print("Goodbye!")
        break
    print("")
