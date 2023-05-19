from flask import Flask
import os
import Redis
import weather
import logging

API_KEY = os.getenv('OPEN_WEATHER_API_KEY')
OPEN_WEATHER_BASE_URL = os.getenv('OPEN_WEATHER_BASE_URL')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
#REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

#logging.basicConfig(level=logging.DEBUG, filename="app.log", format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("app.log")
formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)

redis = Redis.Redis()

redis_client = redis.connect()
weather = weather.Weather()

def is_redis_client(redis):
    if redis.client:
        return True
    else:
        return False
    
def log_no_redis_connection():
    logger.warn("No Redis Connection")
    
def geocode_city(city):

    if redis.client:
        geocoded_city = redis.get_city_geo_data(city)
        return geocoded_city
    else: 
        log_no_redis_connection()
        response = weather.geocode_city(city)
        return response

@app.route('/weather/<city>')
def current_weather(city):
    city_data = geocode_city(city)
    
    lat = str(city_data["lat"])
    lon = str(city_data["lon"])
    if redis.client:
        response = redis.get_city_current_weather(city, lat, lon)
    else:
       log_no_redis_connection()
       response = weather.city_weather(lat, lon)
    return response

@app.route('/weather/fivedays/<city>')
def five_days_weather(city):

    city_data = geocode_city(city)
    lat = str(city_data["lat"])
    lon = str(city_data["lon"])
    if redis.client:
        response = redis.get_city_fivedays_weather(lat,lon)
    else:
        log_no_redis_connection()
        response = weather.five_days_weather(lat,lon)
    return response


if __name__ == '__main__':
    app.run()