# Weather Tree
A First Year Eng Group Project Utilizing APIs to Make Art

![Image of Weather Tree][imgpath]

## Brief Description
The task was to create an art piece that utilized real time API data to either be interactive or reactive to some real world data. 

The Weather Tree utilizes lights and movement to create an artistic display of the weather conditions of various places in the world. 

The trunk and leaves of the tree light up with different colours signaling the temperature and animations play displaying the condition (rain, snow, lightning, etc). The golden orangutan points in the wind direction.


![Image of Weather Tree On][img2path]


## Members and Contributions
- **Vikram Procter** - 3D design for tree, Lead UI, backend, and animation developer

- **Hammad Shakeel** - 3D design for orangutan, and assembly

- **Micheal Lizak** - 3D design for base and orangutan rotation system, assembly

- **Asif Rahman** - Report and Schedule manager, assembly and testing


## How it Works
Durring initialization it connects to a preprogramed wifi network using the on board wifi chip of the *Raspberry Pi Pico*. It fetches current weather data from the [Weather API][apiLink] and starts a refresh timer (to ensure accurate data). 

The guts of the project are written in micropython. The fetched weather data is then parsed. Values for the servo rotation are computed based on wind direction; colour based on temperature; and animation based on weather conditions.

Eached of these parsed values are then displayed on their respective devices using the Pico's IO pins.


## Weather Temperature to LED Colour Algorithm
The LED colour algorithm utilizes a sigmoid function to generate a colour value based on temperature:

$$hue = 41000 + \cfrac{52000}{1+exp({\cfrac{temp-16}{10})}}$$

$$saturation = 255, value = 255$$


## Weather Condition Animation
The animation for each weather condition used a key frame technique. A *keyframe map* held values for brightness and hue at specific key frame times. 

The pico's on board clock would keep track of time elapsed since the last frame of the animation was displayed, and would render the next frame if that time was greater than the frame period.

Linear extrapolation was used to create smooth transistions between key frame values.



[imgpath]: /img/titlepic.jpeg
[img2path]: /img/accentpic.jpeg
[apiLink]: https://www.weatherapi.com/