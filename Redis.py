import redis
import os
import logging
import requests
import json
import weather



REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("app.log")
formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


weather = weather.Weather()
#logging.basicConfig(level=logging.DEBUG, filename="app.log", format="%(asctime)s:%(levelname)s:%(message)s")

class Redis():
    def __init__(self):
        self.host = os.getenv('REDIS_HOST')
        self.port = os.getenv('REDIS_PORT')
        #self.password = os.getenv('REDIS_PASSWORD')
        self.client = None


    def connect(self):
        try:
            self.client = redis.Redis(
                host = self.host,
                port = self.port,
                decode_responses=True,
                #password = self.password,
                db = 0
            )  
            ping = self.client.ping()
            if ping is True:
                logger.info("Successfully connected to Redis")
                return self.client
        except redis.AuthenticationError:
            logger.error("Redis Authentication error")
        except redis.TimeoutError:
            logger.error("Redis connection timeout")
            self.client = None
            return self.client

            

            
    def get_city_geo_data(self, city):
        response = self.client.hgetall("geo_data:"+city)
        if response:
            logger.info(f"Geocode - {city} - Cache hit")
            return response
        else:
            logger.info(f"Geocode - {city} - Cache miss")
            response = weather.geocode_city(city)
            #place = response.json()[0]
            place_data = {
                "name": response["name"],
                "country": response["country"],
                "state": response["state"],
                "lat": response["lat"],
                "lon": response["lon"]
            }
            logger.info(f"Geocode - {city} - Write around")
            self.__set_city_geo_data(city, place_data)
            return place_data


    def __set_city_geo_data(self, city, city_data):
        response = self.client.hmset("geo_data:"+city, city_data)
        return response

    def get_city_current_weather(self, city, lat, lon):
        response = self.client.get("weather:"+city)
        if response:
            logger.info(f"Current Weather - {city} - Cache hit")
            return json.loads(response)
        else:
            logger.info(f"Current Weather - {city} - Cache miss")
            response = weather.city_weather(lat, lon)
            logger.info(f"Current Weather - {city} - Write around")
            self.__set_city_current_weather(city, response)
            return response



    def __set_city_current_weather(self, city, weather):
        response = self.client.set("weather:"+city, json.dumps(weather))
        return response

    def get_city_fivedays_weather(self, city, lat, lon):
        response = self.client.get("fivedays:"+city)
        if response:
            logger.info(f"Five Days Weather - {city} - Cache hit")
            return json.loads(response)
        else:
            logger.info(f"Five Days Weather - {city} - Cache miss")
            response = weather.five_days_weather(lat, lon)
            logger.info(f"Five Days Weather - {city} - Write around")
            self.__set_city_fivedays_weather(city, response)
            return response

    def __set_city_fivedays_weather(self, city,weather):
        response = self.client.set("fivedays:"+city, json.dumps(weather))
        return response 