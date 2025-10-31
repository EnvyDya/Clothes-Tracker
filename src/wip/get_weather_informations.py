"""Module that handles API calls to Meteosource.
Possibility of getting places IDs or local weather of the day.

Raises:
    geocoding.raise_for_status:
        Exception raised if any error code from the API during the geocoding.
    weather.raise_for_status: 
        Exception raised if any error code from the API during weather retrieval.

Returns:
    _type_: 0 if everything went correctly
"""
import os
import sys
from dotenv import load_dotenv
import requests

# Load env var from .env file
load_dotenv()
METEOSOURCE_API_KEY = os.getenv("METEOSOURCE_API_KEY")

# Get APIs endpoints
METEOSOURCE_API_ENDPOINT = 'https://www.meteosource.com/api/v1/free/'
FIND_PLACE_API = 'find_places'
WEATHER_API = 'point'

def get_place_id(place:str) -> str:
    """Uses Meteosource API's to retrieve the place identifier.

    Args:
        place (str): Name of the place you're in.

    Raises:
        geocoding.raise_for_status: Exception raised if any error code from the API.

    Returns:
        str: place identifier given by Meteosource API's.
    """
    # Request on meteosource API
    geocoding = requests.get(
        url = METEOSOURCE_API_ENDPOINT+FIND_PLACE_API,
        params = {
            'text': place,
            'key': METEOSOURCE_API_KEY,
        },
        timeout=10,
    )
    if not geocoding.ok:
        # If response code is not ok (200), print the resulting http error code with description
        raise geocoding.raise_for_status()
    return geocoding.json()[0]["place_id"]

def get_todays_weather(place_id:str) -> dict:
    """Uses Meteosource API's to retrieve the weather of the day on a given place.

    Args:
        place_id (str): Place identifier following the Meteosource API convention.

    Raises:
        weather.raise_for_status:  Exception raised if any error code from the API.

    Returns:
        dict: All the information corresponding to the weather of the day.
    """
    weather = requests.get(
        url = METEOSOURCE_API_ENDPOINT+WEATHER_API,
        params = {
            'place_id': place_id,
            'sections': 'daily',
            'key': METEOSOURCE_API_KEY,
        },
        timeout=10,
    )
    if not weather.ok:
        # If response code is not ok (200), print the resulting http error code with description
        raise weather.raise_for_status()
    weather_informations = weather.json()['daily']['data'][0]
    print(weather_informations)
    return weather_informations


if __name__ == "__main__":
    # Asking localization to user
    city_name = input("Where do you live ? ")
    get_todays_weather(get_place_id(city_name))
    sys.exit()
