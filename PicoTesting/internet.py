import network
import socket
from time import sleep
#from picozero import pico_temp_sensor, pico_led
import machine

# PicoWMac: D8:3A:DD:2B:64:28

#ssid = 'SquirrelsInPants'
#password = 'floortaco8'
ssid = 'airuc-guest'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
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