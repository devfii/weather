import os
import requests


API_KEY = os.getenv('OPEN_WEATHER_API_KEY')
OPEN_WEATHER_BASE_URL = os.getenv('OPEN_WEATHER_BASE_URL')

class Weather:
    def geocode_city(self, city):

            api_url = OPEN_WEATHER_BASE_URL+"/geo/1.0/direct?q="+city+"&limit=5&appid="+API_KEY
            response = requests.get(api_url)
            place = response.json()[0]
            place_data = {
                "name": place["name"],
                "country": place["country"],
                "state": place["state"],
                "lat": place["lat"],
                "lon": place["lon"]
            }

            return place_data

    def city_weather(self, lat, lon):
        api_url = OPEN_WEATHER_BASE_URL+"/data/2.5/weather?lat="+lat+"&lon="+lon+"&units=Metric&appid="+API_KEY
        response = requests.get(api_url).json()
        return response
    
    def five_days_weather(self, lat, lon):
        api_url = OPEN_WEATHER_BASE_URL+"/data/2.5/forecast?&lat="+lat+"&lon="+lon+"&units=Metric&appid="+API_KEY
        response = requests.get(api_url).json()
        return response
