import network
from time import sleep
import machine
import urequests as requests
import json
from io import BytesIO

# PicoWMac: D8:3A:DD:2B:64:28

#ssid = 'SquirrelsInPants'
#password = 'floortaco8'
ssid = 'airuc-guest'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    #wlan.connect(ssid, password)
    wlan.connect(ssid)
    
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
    
try:
    ip = connect()
except KeyboardInterrupt:
    machine.reset()
    


url = 'http://api.weatherapi.com/v1/forecast.json'
tags_url = ''
params = {
    'key': '6d6353bde9e1462f893215306242501',
    'q': 'Calgary',
    'day': '1',
    'aqi': 'no',
    'alerts': 'no'
}
identifiers = params.keys()
param_add = "?"
for identifier in identifiers:
    param_add += f"{identifier}={params[identifier]}&"

param_add = param_add[:-1]

url=url + param_add

response = requests.get(url)
    
if response.status_code == 200:
    weather = response.json()
else:
    print('Request failed with status code:', response.status_code)
    
#file = open("fi.json", 'w')
#json.dump(data, file)
#print("Json File written")

print("Location: " + weather["location"]["name"])
print("Date/Time: " + weather["location"]["localtime"])

response.close()

