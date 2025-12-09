import requests
from typing import Tuple
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import datetime
from zoneinfo import ZoneInfo

DEFAULT_LOCATION = "New York"
DEFAULT_TIMEZONE = "America/New_York"

#given a location string, returns the latitude, longitude, and address
def get_location_details(location: str = DEFAULT_LOCATION) -> Tuple[float,float,str]:
     # Geocode an address
        geolocator = Nominatim(user_agent="cli-dashboard")
        location_data = geolocator.geocode(location)
        if location_data is None:
              return get_location_details(DEFAULT_LOCATION)
        return (location_data.latitude, location_data.longitude, location_data.address)

#given a location string, returns the temperature in F, current weather conditions, and city
def get_weather_details(location: str = DEFAULT_LOCATION) -> Tuple[int,str,str]:
        # Geocode an address
        location_data = get_location_details(location)

        if location_data is None:
            return (None,None,None)
        else:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={location_data[0]}&longitude={location_data[1]}&current_weather=true"
            resp = requests.get(url, timeout=5)
            data = resp.json()
            cw = data.get("current_weather", {})
            temperature = cw.get("temperature")  # in Celsius by default

            # convert to Fahrenheit
            temp_f = int(temperature * 9/5 + 32) if temperature is not None else None

            weather_code = cw.get("weathercode")
            weather_conditions = _map_weather_code(weather_code)

            city = str(location_data[2]).split(",")[0]
            return (temp_f, weather_conditions, city)

#given a meteo weather code, returns the cooresponding weather conditions
def _map_weather_code(code: int) -> str:
        """Map Open-Meteo weather codes to Nerd Font weather icons."""
        mapping = {
            0:  "Clear \uf522",                     # nf-weather-day_sunny
            1:  "Mainly clear \uf522",
            2:  "Partly cloudy \uf522",
            3:  "Overcast \ue312",                  # nf-weather-cloudy

            45: "Fog \ue313",                      # nf-weather-fog
            48: "Depositing rime fog \ue313",

            51: "Light drizzle \ue311",            # nf-weather-showers
            53: "Moderate drizzle \ue311",
            55: "Dense drizzle \ue311",
            56: "Light freezing drizzle \ue30f",   # nf-weather-rain_mix
            57: "Dense freezing drizzle \ue30f",

            61: "Slight rain \ue318",              # nf-weather-rain
            63: "Moderate rain \ue318",
            65: "Heavy rain \ue318",
            66: "Light freezing rain \ue30f",
            67: "Heavy freezing rain \ue30f",

            71: "Slight snow fall \ue31a",         # nf-weather-snow
            73: "Moderate snow fall \ue31a",
            75: "Heavy snow fall \ue31a",
            77: "Snow grains \ue31a",

            80: "Slight rain showers \ue319",      # nf-weather-showers
            81: "Moderate rain showers \ue319",
            82: "Violent rain showers \ue319",

            85: "Slight snow showers \ue319",
            86: "Heavy snow showers \ue319",

            95: "Thunderstorm \ue31d",             # nf-weather-thunderstorm
            96: "Thunderstorm with slight hail \ue318",
            99: "Thunderstorm with heavy hail \ue318",
        }
        return mapping.get(code, "Unknown \uf07b")  # nf-weather-na


def get_timezone(latitude: float, longitude: float) -> ZoneInfo:
      
    # Initialize the TimezoneFinder object
    tf = TimezoneFinder()

    # Get the timezone string
    timezone_str = tf.certain_timezone_at(lat=latitude, lng=longitude)

    if timezone_str is None:
        return None
    else:
        return ZoneInfo(timezone_str)
    
def update_greeting(timezone) -> str:
    hour = datetime.datetime.now(timezone).hour
    if hour < 12:
        text = "Good Morning"
    elif hour < 18:
        text = "Good Afternoon"
    else:
        text = "Good Evening"
    return text

