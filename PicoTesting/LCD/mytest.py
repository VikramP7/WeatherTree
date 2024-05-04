import utime

import machine
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

#lcd = 0

def init_lcd(scd_pin, scl_pin):
    #Test function for verifying basic functionality
    print("Running test_main")
    i2c = I2C(0, sda=machine.Pin(int(scd_pin)), scl=machine.Pin(int(scl_pin)), freq=400000)
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
    utime.sleep(2)
    lcd.clear()
    return lcd
    
lcd = init_lcd(0,1)
lcd.show_cursor()
lcd.blink_cursor_on()
lcd.move_to(5,1)