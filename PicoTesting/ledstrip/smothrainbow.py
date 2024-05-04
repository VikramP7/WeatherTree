from time import sleep
from neopixel import Neopixel
    

numpix = 30
strip = Neopixel(numpix, 0, 2, "RGB")

strip.brightness(255)

hue = 0
saturation = 255
value = 255
while True:
    color = strip.colorHSV(hue, saturation, value)
    strip.fill(color)
    sleep(0.1)
    strip.show()
    
    hue += 200
    #saturation += 1
    #value += 1
    #value = value % 255
    print("Hue:", hue, "Saturation:", saturation, "Value:",value)
