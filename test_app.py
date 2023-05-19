import app
import pytest
import json

response = None

@pytest.fixture(scope="module")
def city():
    with open('city.json','r', encoding="cp866") as city_file:
        cities = json.load(city_file)
    city = cities[0]
    return city


def test_geocode_city(city):
    assert city["name"] == "London"
    assert city["lat"] == 51.5073219
    assert city["lon"] == -0.1276474
    assert city["country"] == "GB"
    assert city["state"] == "England"



