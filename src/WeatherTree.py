# LED Strip
from neopixel import Neopixel
from animation import Animation

# Internet
import network
import socket

# API Stuffs
import urequests as requests
import json
from io import BytesIO
from WeatherApi import WeatherApi

# Servo
from Servo import Servo

# LCD
import utime
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# General
from time import sleep
from machine import Pin, PWM
import math
import random


# Machine Constants

# Button
button_pin = 27

# Led Strip
led_number_of_leds = 30 # number of leds
brightness = 255 # brightness of strip
led_strip_pin = 2 # Din GPIO pin
animation_snow_grouping = 6
animation_rain_dribble = 1
animation_thunderness = 50


# Internet
# PicoWMac: D8:3A:DD:2B:64:28
ssid = 'airuc-guest' # university of Calgary
#ssid = 'SHANKOBARI'
#password ='WhiffleSword'
wifi_connected = False


# API
my_api_key = '6d6353bde9e1462f893215306242501'
cities = ['Calgary','Karachi','New York','Dhaka','Barcelona', 'Newcastle AU', 'Gdansk', 'Kolkata']
max_weather_age = 10 * 60 # seconds

# Servo
servo_pwm_pin = 22
servo_pwm_frequency = 50 # Hz
max_servo_angle = 180 # degrees
min_servo_duty = 1640
max_servo_duty = 7864

# LCD
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
lcd_sda_pin  = 0
lcd_scl_pin  = 1

# Random Stuff
demo_mode = 0
sigmoid = lambda x: (1/(1+math.exp(-x)))

def init_led_strip(numpix=30):
    strip = Neopixel(numpix, 0, led_strip_pin, "RGB")
    strip.brightness(brightness)
    strip.fill((255,0,0))
    strip.show()
    return strip


def wifi_connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid)#, password)
    
    try_count = 0
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
        try_count += 1
        if try_count > 30:
            raise Exception("Wifi Failed to connected within 10 seconds")
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
    
    try:
        ip = connect()
    except KeyboardInterrupt:
        machine.reset()
    


def init_servo(pwm_pin=servo_pwm_pin, pwm_frequency=servo_pwm_frequency):
    servo = Servo(pwm_pin, pwm_frequency, 0, max_servo_angle, min_servo_duty, max_servo_duty)
    return servo


def init_api():
    weather = WeatherApi(cities, my_api_key)
    return weather
    

def init_lcd(sda_pin=lcd_sda_pin, scl_pin=lcd_scl_pin):
    i2c = I2C(0, sda=machine.Pin(int(sda_pin)), scl=machine.Pin(int(scl_pin)), freq=400000)
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
    utime.sleep(2)
    lcd.clear()
    return lcd


def linear_temp_to_colour(temp, strip):
    # angle range 0-285
    temp_fraction = (temp + 30)/60
    hue = 41000 + int(temp_fraction * (65535*(285/360)))
    colour = strip.colorHSV(hue, 255, 255)
    return colour

def sigmoid_temp_to_colour(temp, strip):
    temp = temp if temp < 37 else 37
    hue = 41000 + int(52000*sigmoid((temp-16)/10))
    colour = strip.colorHSV(hue, 255, 255)
    return colour

def sigmoid_temp_to_hue(temp):
    temp = temp if temp < 37 else 37
    hue = 41000 + int(52000*sigmoid((temp-16)/10))
    return hue
    

def main():
    # init the led strip
    led_strip = init_led_strip(led_number_of_leds)
    animation = Animation(led_number_of_leds, animation_snow_grouping, animation_rain_dribble, animation_thunderness)
    print("Led Strip Initialized")
    
    # init LCD
    lcd = init_lcd()
    print("LCD Initialized")
    
    # init button
    button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)
    print("Button Initialized")
    
    # init the servo
    servo = init_servo(servo_pwm_pin, servo_pwm_frequency)
    print("Servo Initialized")
    servo.move(0)
    
    # connect to the wifi
    wifi_connected = False
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("Wifi Connecting")
    try:
        wifi_connect()
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("Wifi Connected")
        wifi_connected = True
        print("Wifi Connected")
    except:
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("Wifi Failed")
        lcd.move_to(0,1)
        lcd.putstr("To Connect")
        """
        sleep(5)
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("Entering")
        lcd.move_to(0,1)
        lcd.putstr("Demo Mode")
        demo_mode = 1
        """
    
    # init weather api
    if wifi_connected:
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("Loading Weather")
        weather = init_api()
        print("Weather Api Fetched")
    
    # define useful things for running loop
    city_index = 0
    current_city = cities[city_index]
    lcd_top_text = ""
    lcd_bottom_text = ""
    cur_servo_dir = 0
    led_frame_period = 50 # ms
    last_frame = 0
    led_temp_colour = 0
    dimness = 0
    up = True
    # enter the running loop
    while True: #demo_mode == 0:
        # Fetch the weather
        current_city = cities[city_index]
        temp, wind_dir, condition, precipitation = weather.get_city_weather(current_city)
        condition = condition.lower()
        condition = condition.replace("drizzle", "rain")
        condition = condition.replace("blizzard", "snow")
        condition = condition.replace("sleet", "snow")
        if city_index == 2:
            condition = "thunder"
        elif city_index == 1:
            condition = "rain"
        
        # Display LCD message
        # Displays the city name and the temperature
        if (lcd_top_text != current_city):
            # clear line
            lcd.move_to(0,0)
            lcd.putstr(' '*16)
            # calculate center
            first_char = int((16-len(current_city))/2)
            # display city name
            lcd.move_to(first_char,0)
            lcd.putstr(current_city)
            # preform book keeping
            lcd_top_text = current_city
            print("LCD Top: " + lcd_top_text)
            print("Condition:", condition)
            
            
        if (lcd_bottom_text[:-2] != str(temp)):
            # clear line
            lcd.move_to(0,1)
            lcd.putstr(' '*16)
            # calculate center
            first_char = int((16-len(str(temp))-2)/2)
            # display temperature
            lcd.move_to(first_char,1)
            bottom_text = str(temp) + (chr(223)) + "C" # "\u00B0"
            lcd.putstr(bottom_text)
            # preform book keeping
            lcd_bottom_text = bottom_text
            print("LCD Bottom: " + lcd_bottom_text)
        
        # Rotate the servo to wind dirrection
        if int(cur_servo_dir) != int(wind_dir):
            servo.move(wind_dir/2)
            cur_servo_dir = wind_dir
            print('Wind direction ' + str(wind_dir))
        
        if button.value():
            print("Button Pressed")
            # run Selection Menu
            # Clear LCD
            lcd.clear()
            lcd_top_text = ""
            lcd_bottom_text = ""
            
            # Increment Current City
            city_index += 1
            city_index = city_index % len(cities)
            
            
            
        # Do LED animation
        cur_time = utime.ticks_ms()
        if abs(last_frame - cur_time) > led_frame_period:
            last_frame = cur_time
            # step fram animate to next frame
            # Determine hue based on temperature
            hue = sigmoid_temp_to_hue(temp)
            
            # determine value based on weather condition
            if condition.lower().find("thunder") != -1:
                # flashing like lighnting and breif yellow pixels
                led_colours = animation.next_thunder_frame(hue)
                for led in range(len(led_colours)):
                    cur_colour = led_strip.colorHSV(led_colours[led][0], led_colours[led][1], led_colours[led][2])
                    led_strip.set_pixel(led, cur_colour)
            elif condition.lower().find("rain") != -1:
                # Flowing down
                # or random dots fading
                for led in range(led_number_of_leds):
                    value = animation.next_rain_frame(led)
                    cur_colour = led_strip.colorHSV(hue, 255, value)
                    led_strip.set_pixel(led, cur_colour)
                animation.advance_rain_frame() 
            elif condition.lower().find("snow") != -1:
                # moderate fade in and out broken into sections
                for led in range(led_number_of_leds):
                    value = animation.next_snow_frame(led)
                    cur_colour = led_strip.colorHSV(hue, 255, value)
                    led_strip.set_pixel(led, cur_colour)
                animation.advance_snow_frame()
            else: # clear weather conditions
                value = animation.next_clear_frame()
                cur_colour = led_strip.colorHSV(hue, 255, value)
                led_strip.fill(cur_colour)
            led_strip.show()
    
    monkey_angle = 0
    monkey_up = True
    while demo_mode == 1:
        for led in range(led_number_of_leds):
            hue = random.randint(0,255)
            led_strip.set_pixel(led, led_strip.colorHSV(hue, 255, 255))
        servo.move(monkey_angle)
        monkey_angle += 2 if monkey_up else -2
        if monkey_angle <= 0:
            monkey_up = True
        elif monkey_angle >= 180:
            monkey_up = False
        sleep(0.1)
    
    
if __name__ == "__main__":
    main()
