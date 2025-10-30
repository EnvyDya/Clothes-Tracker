from datetime import datetime
from dotenv import load_dotenv
import os
import re
import requests

# Load env var from .env file
load_dotenv()

# Get APIs endpoints
METEOSOURCE_API_ENDPOINT = 'https://www.meteosource.com/api/v1/free/'
FIND_PLACE_API = 'find_places'
WEATHER_API = 'point'

if __name__ == "__main__":
    # Recover API Key from environment variable
    meteosource_api_key = os.getenv("METEOSOURCE_API_KEY")

    # Printing prediction date
    today = datetime.today()
    print(f"Predicting for the date of {today.date()}.")

    # Asking localization to user
    city_name = input("Where do you live ? ") # TODO: Prevent injections in API request
    params_geocoding = {
        'text': city_name,
        'key': meteosource_api_key,
    }
    geocoding = requests.get(METEOSOURCE_API_ENDPOINT+FIND_PLACE_API, params_geocoding)
    if geocoding.ok:
        city_informations = geocoding.json()[0]
        params_weather = {
            'place_id': city_informations["place_id"],
            'sections': 'daily',
            'key': meteosource_api_key,
        }
        weather = requests.get(METEOSOURCE_API_ENDPOINT+WEATHER_API, params_weather)
        if weather.ok:
            weather_informations = weather.json()['daily']['data'][0]
            print(weather_informations)
        else:
            weather.raise_for_status()
    else:
        # If response code is not ok (200), print the resulting http error code with description
        geocoding.raise_for_status()
        