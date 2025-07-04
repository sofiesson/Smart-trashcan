from machine import Pin
from utime import sleep
from dht import DHT11

class TempHumSensor:
    def __init__(self, pin=6):
        self.sensor = DHT11(Pin(pin, Pin.IN, Pin.PULL_UP))
    
    def read(self):
        try:
            self.sensor.measure()
            temp = self.sensor.temperature()
            humi = self.sensor.humidity()
            return temp, humi
        except Exception as e:
            print(f"Sensor read error: {e}")
            return None, None
    
    def print_values(self):
        temp, humi = self.read()
        if temp is not None and humi is not None:
            print(f"Temperature: {temp}°C   Humidity: {humi:.0f}%")
        else:
            print("Failed to read sensor data.")
