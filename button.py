import RPi.GPIO as GPIO
import time
import config

class Button:
    def __init__(self, pin):
        print(f"[ BUTTON.PY ] Initializing button on pin {pin}")
        self.pin = pin
        self._callback = None
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self._push, bouncetime=config.bouncetime)
        
    def register_callback(self, callback_func):
        print(f"[ BUTTON.PY ] Registered callback function for button on pin {self.pin}")
        self._callback = callback_func
        
    def _push(self, channel):
        print(f"[ BUTTON.PY ] Button pushed - pin {self.pin}")
        if self._callback:
            print("[ BUTTON.PY ] Running callback function")
            self._callback()