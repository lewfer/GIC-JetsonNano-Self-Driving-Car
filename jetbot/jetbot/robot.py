import time
import RPi.GPIO as GPIO

import traitlets
from traitlets.config.configurable import SingletonConfigurable


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
class Robot(SingletonConfigurable):
    
    # Values to link to a game controller
    left_motor_value = traitlets.Float()
    right_motor_value = traitlets.Float()
        
    def __init__(self, *args, **kwargs):
        super(Robot, self).__init__(*args, **kwargs)
        
        # Drive pins
        self.left_motor = [35,36] # HIGH/LOW for forward, LOW/HIGH for backward, LOW/LOW for stop
        self.right_motor = [37,38] # HIGH/LOW for forward, LOW/HIGH for backward, LOW/LOW for stop
        GPIO.setup(self.left_motor[0],GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.right_motor[0],GPIO.OUT,initial=GPIO.LOW) 
        GPIO.setup(self.left_motor[1],GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.right_motor[1],GPIO.OUT,initial=GPIO.LOW) 
        
        # Enable (PWM) pins
        GPIO.setup(32,GPIO.OUT) # LEFT
        GPIO.setup(33,GPIO.OUT) # RIGHT
        self.pwm=[GPIO.PWM(32,50),GPIO.PWM(33,50)]
        
        # Start PWM
        self.pwm[0].start(0)
        self.pwm[1].start(0)
        
    # Respond to game controller
    @traitlets.observe('left_motor_value')
    def _observe_left_motor_value(self, change):
        #self._write_value(change['new'])
        print("left change", change['new'])
        self.left_motor_value = change['new']
        self.set_motors(left_speed=self.left_motor_value, right_speed=self.right_motor_value)
        
    # Respond to game controller
    @traitlets.observe('right_motor_value')
    def _observe_right_motor_value(self, change):
        #self._write_value(change['new'])
        print("right change", change['new'])
        self.right_motor_value = change['new']
        self.set_motors(left_speed=self.left_motor_value, right_speed=self.right_motor_value)
        
    
    def set_motors(self, left_speed=1.0, right_speed=1.0):
        # Scale to range 0 to 100
        left_speed = int(left_speed*100) 
        right_speed = int(right_speed*100) 
        
        if left_speed>0:
            GPIO.output(self.left_motor[0],GPIO.HIGH)
            GPIO.output(self.left_motor[1],GPIO.LOW)
        elif left_speed<0:
            GPIO.output(self.left_motor[0],GPIO.LOW)
            GPIO.output(self.left_motor[1],GPIO.HIGH)
            left_speed = -left_speed
        else:
            GPIO.output(self.left_motor[0],GPIO.LOW)
            GPIO.output(self.left_motor[1],GPIO.LOW)  
            
        if right_speed>0:
            GPIO.output(self.right_motor[0],GPIO.HIGH) 
            GPIO.output(self.right_motor[1],GPIO.LOW) 
        elif right_speed<0:
            GPIO.output(self.right_motor[0],GPIO.LOW) 
            GPIO.output(self.right_motor[1],GPIO.HIGH) 
            right_speed = -right_speed
        else:
            GPIO.output(self.right_motor[0],GPIO.LOW) 
            GPIO.output(self.right_motor[1],GPIO.LOW) 
            
        self.pwm[0].ChangeDutyCycle(left_speed)
        self.pwm[1].ChangeDutyCycle(right_speed)
        
    def forward(self, speed=1.0, duration=None):
        GPIO.output(self.left_motor[0],GPIO.HIGH)
        GPIO.output(self.left_motor[1],GPIO.LOW)
        GPIO.output(self.right_motor[0],GPIO.HIGH) 
        GPIO.output(self.right_motor[1],GPIO.LOW) 
        speed = int(speed*100)
        self.pwm[0].ChangeDutyCycle(speed)
        self.pwm[1].ChangeDutyCycle(speed)
        
    def backward(self, speed=1.0):
        GPIO.output(self.left_motor[0],GPIO.LOW)
        GPIO.output(self.left_motor[1],GPIO.HIGH)
        GPIO.output(self.right_motor[0],GPIO.LOW) 
        GPIO.output(self.right_motor[1],GPIO.HIGH) 
        speed = int(speed*100)
        self.pwm[0].ChangeDutyCycle(speed)
        self.pwm[1].ChangeDutyCycle(speed)
        
    def left(self, speed=1.0):
        GPIO.output(self.left_motor[0],GPIO.LOW)
        GPIO.output(self.left_motor[1],GPIO.HIGH)
        GPIO.output(self.right_motor[0],GPIO.HIGH) 
        GPIO.output(self.right_motor[1],GPIO.LOW) 
        speed = int(speed*100)
        self.pwm[0].ChangeDutyCycle(speed)
        self.pwm[1].ChangeDutyCycle(speed)
        
    def right(self, speed=1.0):
        GPIO.output(self.left_motor[0],GPIO.HIGH)
        GPIO.output(self.right_motor[0],GPIO.LOW) 
        GPIO.output(self.left_motor[1],GPIO.LOW)
        GPIO.output(self.right_motor[1],GPIO.HIGH) 
        speed = int(speed*100)
        self.pwm[0].ChangeDutyCycle(speed)
        self.pwm[1].ChangeDutyCycle(speed)
        
    def stop(self):
        GPIO.output(self.left_motor[0],GPIO.LOW)
        GPIO.output(self.left_motor[1],GPIO.LOW)
        GPIO.output(self.right_motor[0],GPIO.LOW) 
        GPIO.output(self.right_motor[1],GPIO.LOW) 
        self.pwm[0].ChangeDutyCycle(0)
        self.pwm[1].ChangeDutyCycle(0)
        