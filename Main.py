from adafruit_io import AdafruitIO
from config import AIO_FEEDS
from servo_controller import ServoController
from ultrasonic import UltrasonicSensor
from temphumsensor import TempHumSensor
from obstaclesensor import ObstacleSensor
from machine import Pin
import utime

ultrasonic = UltrasonicSensor(trigger_pin=3, echo_pin=2)
servo = ServoController(servo_pin=0)
temp_hum_sensor = TempHumSensor(pin=6)
obstacle_sensor = ObstacleSensor(pin=1)
Red = Pin(15, Pin.OUT)
Green = Pin(14, Pin.OUT)

obstacle_starttime = None
Trash_Fulltime = 5
last_lid_state = None
last_obstacle_state = None
last_publish_time = 0
PUBLISH_INTERVAL = 30

try:
    ip = connect()
except Exception as e:
    print("Failed to connect to WiFi:", e)
    
adafruit = AdafruitIO()

print("Connecting to Adafruit IO...")
if not adafruit.connect():
    print("Warning: Couldn't connect to Adafruit IO")

while True:
    current_time = utime.time()
    distance = ultrasonic.measure_distance()
    obstacle_detected = obstacle_sensor.detect()

    # Lid to open/close
    current_lid_state = "open" if distance <= 10 else "closed"
    if current_lid_state != last_lid_state:
        adafruit.publish(AIO_FEEDS["lid"], current_lid_state)
        last_lid_state = current_lid_state
        print(f"Lid state changed to: {current_lid_state}")

    # servo motor
    if current_lid_state == "open":
        Green.value(1)
        Red.value(0)
        servo.set_angle(0)
    else:
        Red.value(1)
        Green.value(0)
        servo.set_angle(90)
    
    # Obstacle detection
    current_obstacle_state = None
    if obstacle_detected:
        if obstacle_starttime is None:
            obstacle_starttime = current_time
        elif current_time - obstacle_starttime >= Trash_Fulltime:
            current_obstacle_state = "full"
    else:
        current_obstacle_state = "not_full"
        obstacle_starttime = None

    if current_obstacle_state is not None and current_obstacle_state != last_obstacle_state:
        adafruit.publish(AIO_FEEDS["trashstat"], current_obstacle_state)
        last_obstacle_state = current_obstacle_state
        
    # temperature and humidity 
    temp, hum = temp_hum_sensor.read()
    if temp is not None and hum is not None:
        adafruit.publish(AIO_FEEDS["temp"], temp)
        adafruit.publish(AIO_FEEDS["hum"], hum)

    utime.sleep(3)
