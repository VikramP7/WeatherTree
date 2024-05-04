from machine import Pin, PWM, ADC
from time import sleep

pwm = PWM(Pin(0))
adc = ADC(Pin(28)) # 224-65535

pwm.freq(50)

angle = 0

while True:
    #pwm.duty_u16(0)
    #sleep(0.0001)
    #pwm.duty_u16(3251)
    #sleep(1)
    
    read = adc.read_u16()
    read = ((read - 224)/65535)*(7864-1600)
    read = read + 1600
    pwm.duty_u16(int(read))
    
    """
    for duty in range(1600, 7864, 100):
        pwm.duty_u16(duty)
        print(duty)
        sleep(0.1)
    
    for duty in range(6502, 0, -1):
        pwm.duty_u16(duty)
        sleep(1)
    """