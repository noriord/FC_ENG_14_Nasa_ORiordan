# Terminal : entered "pip install requests"
# in Terminal, run pip freeze > maymay19thhomework_requirements.txt

import requests
from datetime import datetime, timedelta
import json
import os

# File to store query results
CACHE_FILE = "weather_cache.json"


# Load cache from file
def load_cache():
    if os.path.exists(CACHE_FILE):
        file = open(CACHE_FILE, "r")
        data = json.load(file)
        file.close()
        return data
    return {}


# Save cache to file
def save_cache(cache):
    file = open(CACHE_FILE, "w")
    json.dump(cache, file)
    file.close()


# Main program
print("=" * 40)
print("  Weather Rain Checker")
print("=" * 40)

while True:
    # Step 1: Get date from user
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

    # Step 2: Get city name from user
    city = input("Enter a city name (e.g. Cork): ").strip()

    if city == "":
        print("No city entered. Try again.")
        continue

    # Step 3: Use geocoding API to get latitude and longitude from city name
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

    # Step 4: Check cache first
    cache = load_cache()
    cache_key = latitude + "_" + longitude + "_" + searched_date

    if cache_key in cache:
        print("")
        print("[Loaded from cache - no API call needed]")
        precipitation = cache[cache_key]
    else:
        # Step 5: Make weather API request
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

        # Save to cache
        cache[cache_key] = precipitation
        save_cache(cache)

    # Step 6: Show result
    # Using shorthand conditional from class
    result = "It will rain" if precipitation is not None and precipitation > 0.0 else "It will not rain" if precipitation is not None and precipitation == 0.0 else "I don't know"

    print("")
    print("Date: " + searched_date)
    print("City: " + city_name + ", " + country)
    print("Result: " + result)

    if precipitation is not None and precipitation > 0.0:
        print("Precipitation: " + str(precipitation) + " mm")

    # Ask to continue
    print("")
    again = input("Check another? (yes/no): ").strip().lower()
    if again != "yes" and again != "y":
        print("Goodbye!")
        break
    print("")