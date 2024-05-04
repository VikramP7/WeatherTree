from machine import Pin, PWM, ADC
from time import sleep

# ADC 0-65535
# 224 - 43930

adc = ADC(Pin(27))
led = PWM(Pin(13))

led.freq(1000)

while True:
    led.duty_u16(adc.read_u16())
    print((adc.read_u16()/1))
    sleep(0.1)