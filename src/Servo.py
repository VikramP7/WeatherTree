from machine import Pin, PWM

# machine PWM duty run in range 0-65025

class Servo():
    
    def __init__(self, pwm_pin, servo_pwm_freq=50, min_angle=0, max_angle=180, min_duty = 1640, max_duty = 7864):
        self.pwm = PWM(Pin(int(pwm_pin)))
        self.freq = servo_pwm_freq
        self.pwm.freq(self.freq)
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.min_u16_duty = min_duty
        self.max_u16_duty = max_duty
        self.angle_conversion_factor = (self.max_u16_duty - self.min_u16_duty) / (self.max_angle - self.min_angle)
        self.current_angle = 0.001
        
    def update_settings(self, servo_pwm_freq, min_angle=0, max_angle=180, min_duty = 1640, max_duty = 7864):
        self.freq = servo_pwm_freq
        self.min_u16_duty = min_u16_duty
        self.max_u16_duty = max_u16_duty
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.angle_conversion_factor = (self.max_u16_duty - self.min_u16_duty) / (self.max_angle - self.min_angle)
        
    def move(self, angle):
        # round to 2 decimal places, so we have a chance of reducing unwanted servo adjustments
        angle = round(angle, 2)
        # do we need to move?
        if angle == self.current_angle:
            print("Frack")
            return
        self.current_angle = angle
        # calculate the new duty cycle and move the motor
        duty_u16 = self.__angle_to_u16_duty(angle)
        #print(duty_u16)
        self.pwm.duty_u16(duty_u16)
        print("Servo Moved to " + str(angle))
    
    def __angle_to_u16_duty(self, angle):
        return int((angle - self.min_angle) * self.angle_conversion_factor) + self.min_u16_duty
        