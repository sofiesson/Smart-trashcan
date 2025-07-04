from machine import Pin
from time import sleep

class ObstacleSensor:
    def __init__(self, pin=1):
        self.sensor = Pin(pin, Pin.IN, Pin.PULL_DOWN)
    
    def detect(self):
        return self.sensor.value() == 0
    
    def monitor(self, callback=None, interval=0.5):
        last_state = None
        while True:
            current_state = self.detect()
            if callback and current_state != last_state:
                callback(current_state)
            last_state = current_state
            sleep(interval)
