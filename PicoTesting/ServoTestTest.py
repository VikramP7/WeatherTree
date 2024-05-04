from machine import Pin, PWM, ADC
from time import sleep

pwm = PWM(Pin(22))
#adc = ADC(Pin(28)) # 224-65535

pwm.freq(50)

angle = 0

while True:
    for duty in range(1600, 7864, 100):
        pwm.duty_u16(duty)
        print(duty)
        sleep(0.1)
    """
    for duty in range(6502, 0, -1):
        pwm.duty_u16(duty)
        sleep(0.11)
    """