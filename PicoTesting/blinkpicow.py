from machine import Pin, PWM
from time import sleep

led = Pin("LED", Pin.OUT)
led2 = Pin(0, Pin.OUT)
button = Pin(1,Pin.IN, Pin.PULL_UP)

on = 0

while True:
    if(not button.value()):
        led2.toggle()
    print(button.value())
    sleep(0.2)
    
    #led.toggle()
    