import requests
import sys
import re
# import datetime

class Locate:
    def __init__(self, location):
        self.location = location
        self._latitude = None
        self._longitude = None

    def __str__(self):
        return f"The coordinates of {self.location} are {self._latitude} {self._longitude}"
    
    def lat_long(self):
        # Get latitude and longitude if input is in zipcode format
        if re.search(r"^([0-9]{5})$", self.location):
            url_zip = f"https://api.zippopotam.us/us/{self.location}"
            response = requests.get(url_zip)
            if response.status_code == 200:
                zip_data = response.json()
                if zip_data:
                    latitude = round(float(zip_data["places"][0]["latitude"]), 4)
                    longitude = round(float(zip_data["places"][0]["longitude"]), 4)
                    self._latitude = latitude
                    self._longitude = longitude
                    return latitude, longitude
                else:
                    sys.exit("No results found for the specified location")
            else:
                sys.exit("Error fetching data")
        # Get latitude and longitude if input is in City, State format
        elif re.search(r"^[a-z ]+,[a-z ]+$", self.location):
            url_city_state = "https://nominatim.openstreetmap.org/search"
            params = {"q":self.location, "format":"json"}
            response = requests.get(url_city_state, params = params)
            if response.status_code == 200:
                city_state_data = response.json()
                if city_state_data:
                    latitude = round(float(city_state_data[0]["lat"]), 4)
                    longitude = round(float(city_state_data[0]["lon"]), 4)
                    self._latitude = latitude
                    self._longitude = longitude
                    return latitude, longitude
                else:
                    sys.exit("No results found for the specified location")
            else:
                sys.exit("Error fetching location data")
        else:
            sys.exit("Invalid Location Format. Input was not a valid zipcode or City/State")

class WeatherAPI:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return f"The provided coordinates are {self.lat} {self.lon}"
    
    def general_forecast(self):
        noaa_url = f"https://api.weather.gov/points/{self.lat},{self.lon}"
        noaa_response = requests.get(noaa_url)
        if noaa_response.status_code == 200:
            forecast_url = noaa_response.json()["properties"]["forecast"]
        else:
            sys.exit("Error fetching data from weather API")

        forecast_response = requests.get(forecast_url)
        if forecast_response.status_code == 200:
            raw_data = forecast_response.json()["properties"]
            # elevation = raw_data["elevation"] # in meters
            # weather_data = raw_data["periods"]
            return raw_data
        else:
            sys.exit("Error fetching forecast data")


class WeatherData:
    def __init__(self, raw, loc, degree = "F"):
        self._raw = raw
        self.degree = degree
        self._location = loc.title()

    def __str__(self):
        return f"Today in {self._location}: {self._raw['periods'][0]['detailedForecast']}"


# request a location from a user
def main():
    l = input("Please provide either a zip code (i.e., 12345) or a city and state (i.e., Seattle, Washington): ").strip().lower()
    #deg = input("Would you like the temperature in Fahrenheit or Celsius? (F/C): ")
    position = Locate(l)
    lat, long = position.lat_long()
    #print(lat, long)
    #print(str(position))
    weather = WeatherAPI(lat, long)
    raw_data = weather.general_forecast()
    forecast = WeatherData(raw_data, l)
    print(str(forecast))

if __name__ == "__main__":
    main()