import RPi.GPIO as GPIO
import config
from config import State

class LEDController:
    def __init__(self, red_pin, green_pin, blue_pin):
        self.red = red_pin
        self.green = green_pin
        self.blue = blue_pin
        
        GPIO.setup(self.red, GPIO.OUT)
        GPIO.setup(self.green, GPIO.OUT)
        GPIO.setup(self.blue, GPIO.OUT)
        
        self.all_off()
        
    def all_off(self):
        GPIO.output(self.red, GPIO.LOW)
        GPIO.output(self.green, GPIO.LOW)
        GPIO.output(self.blue, GPIO.LOW)
        
    def set_state(self, state):
        self.all_off()
        if state == State.LISTENING:
            GPIO.output(self.green, GPIO.HIGH)
        elif state == State.THINKING:
            GPIO.output(self.red, GPIO.HIGH)
        elif state == State.SPEAKING:
            GPIO.output(self.blue, GPIO.HIGH)