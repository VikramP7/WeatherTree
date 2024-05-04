import requests
import json
from PIL import Image
from io import BytesIO

url = 'http://api.weatherapi.com/v1/forecast.json'
tags_url = ''
params = {
    'key': '6d6353bde9e1462f893215306242501',
    'q': 'Calgary',
    'day': '1',
    'aqi': 'no',
    'alerts': 'no'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
else:
    print('Request failed with status code:', response.status_code)
    
file = open("fi.json", 'w')
json.dump(data, file)
print("Json File written")

print("Location: " + data["location"]["name"])
print("Date/Time: " + data["location"]["localtime"])

