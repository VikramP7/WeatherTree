#import math
import random

class Animation():
    
    def __init__(self, number_of_leds, snow_grouping, rain_dribble, thunderness):
        # animation length is 60 frames
        self.animation_length = 60
        self.number_of_leds = number_of_leds
        
        self.snow_grouping = snow_grouping
        self.snow_frame = 0
        self.snow_animation_value  = [20,255,20]
        self.snow_animation_time   = [0,30, 60]
        self.snow_group_delays = []
        for i in range(number_of_leds//snow_grouping):
            self.snow_group_delays.append(random.randint(0, self.animation_length))
        
        self.rain_dribble = rain_dribble
        self.rain_drop_delays = []
        for i in range(number_of_leds):
            self.rain_drop_delays.append(random.randint(0, self.animation_length))
            
        self.rain_frame = 0
        self.rain_animation_value    = [0,255, 0,255, 0]
        self.rain_animation_time     = [0,10 ,30, 40,60]
        
        self.thunderness = thunderness
        self.thunder_frame = 0
        self.thunder_animation_value  = [100,255,100,255, 0]
        self.thunder_animation_time   = [  0,  8, 12, 14,26]
        self.thunder_animation_length = self.thunder_animation_time[-1]
        self.doing_thunder = False
        self.lightning_colour = (459, 255, 255)
        
        
        
    def linear_tweening(self, cur_frame, last_frame_value, last_frame_time, next_frame_value, next_frame_time):
        # f(t) = mt + b
        slope = (next_frame_value-last_frame_value)/(next_frame_time-last_frame_time)
        b = last_frame_value-(slope*last_frame_time)
        tween_value = (slope*(cur_frame-0)) + b
        return tween_value
    
    
    def quadratic_tweening(self, cur_frame, last_frame_value, last_frame_time, next_frame_value, next_frame_time, b=1):
        # f(t) = (b(t-a)^2) + c
        a = (last_frame_value-next_frame_value-(last_frame_time**2)+(next_frame_time**2))/(-2*(last_frame_time-last_frame_time))
        c = last_frame_value - ((last_frame_time-a)**2)
        tween_value = (1*(cur_frame-a)**2) + c
        return tween_value
        
    
    def position_in_frame_map(self, cur_frame, time_list):
        last_key_frame_index = -1
        next_key_frame_index = -1
        for index in range(len(time_list)-1):
            if cur_frame > time_list[index] and cur_frame < time_list[index+1]:
                last_key_frame_index = index
        if len(time_list)-1 == last_key_frame_index:
            next_key_frame_index = 0
        else:
            next_key_frame_index = last_key_frame_index + 1
        
        return last_key_frame_index, next_key_frame_index
        
    
    def next_animation_frame(self, cur_frame, key_frame_values, key_frame_times):
        
        new_cur_frame = (cur_frame) % key_frame_times[-1]
        
        last_frame, next_frame = self.position_in_frame_map(new_cur_frame, key_frame_times)
       
        try:
            val_index = key_frame_times.index(new_cur_frame)
            value = key_frame_values[val_index]
        except ValueError:
            value = self.linear_tweening(new_cur_frame, key_frame_values[last_frame], key_frame_times[last_frame],
                                         key_frame_values[next_frame], key_frame_times[next_frame])
        #print(value)
        return int(value)
        
    def next_snow_frame(self, pixel_number):
        pixel_number = pixel_number % self.number_of_leds
        
        frame_offset = (pixel_number // self.snow_grouping) + self.snow_group_delays[pixel_number // self.snow_grouping]
        #print(frame_offset)
        
        new_cur_frame = (self.snow_frame+frame_offset) % self.animation_length
        
        value = self.next_animation_frame(new_cur_frame, self.snow_animation_value, self.snow_animation_time)
        #print(value)
        return int(value)
    
    
    def advance_snow_frame(self):
        self.snow_frame += 1
        self.snow_frame = self.snow_frame % self.animation_length
        
    def get_snow_frame(self):
        return self.snow_frame
        
        
    def next_rain_frame(self, pixel_number):
        pixel_number = pixel_number % self.number_of_leds
        
        frame_offset = self.rain_drop_delays[pixel_number]
        new_cur_frame = (self.rain_frame+frame_offset) % self.animation_length
        
        value = self.next_animation_frame(new_cur_frame, self.rain_animation_value, self.rain_animation_time)
        
        return int(value)
    
    def advance_rain_frame(self):
        self.rain_frame += 1*self.rain_dribble
        self.rain_frame = self.rain_frame % self.animation_length
       
       
    def get_rain_frame(self):
        return self.rain_frame
        
    def next_thunder_frame(self, hue):
        # randomly find when lighnting should go
        # play lightning animation on few of pixels and dim rest
        # then play thunder frames later
        led_colours = []
        if (not self.doing_thunder) and random.randint(1000) < self.thunderness:
            # start the thunder protocol
            self.doing_thunder = True
            lightning_led = random.randint(1, self.number_of_leds)
            for led in range(self.number_of_leds):
                if (led == lightning_led) or (led == lightning_led-1):
                    cur_colour = self.lightning_colour
                else:
                    cur_colour = (hue, 255, 100)
                led_colours.append(cur_colour)
        elif self.doing_thunder:
            # lightning has occured
            # based on thunder timer do stuff
            for led in range(self.number_of_leds):
                new_cur_frame = (self.thunder_frame) % self.thunder_animation_length
        
                value = self.next_animation_frame(new_cur_frame, self.thunder_animation_value, self.thunder_animation_time)
                led_colours.append(hue, 255, value)
            # Increment thunder frame
            thunder_frame += 1
            # check if thunder animation is over
            self.doing_thunder = thunder_frame == self.thunder_animation_length+1
            thunder_frame = thunder_frame * int(self.doing_thunder)
        else:
            # rain animation
            for led in range(self.number_of_leds):
                value = next_rain_frame(led)
                led_colours.append(hue, 255, value)
        return led_colours
        
    def next_clear_frame(self):
        return 255
        
        