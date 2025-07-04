from machine import Pin, PWM
from time import sleep

class ServoController:
    def __init__(self, servo_pin=0):
        self.servo_pin = Pin(servo_pin)
        self.servo = PWM(self.servo_pin)
        self.servo.freq(50)
        self.max_duty = 4915  # 90°
        self.min_duty = 1802  # 0°

    def set_angle(self, angle):
        if angle == 0:
            self.servo.duty_u16(self.min_duty)
            print("Servo at 0° (UP)")
        else:
            self.servo.duty_u16(self.max_duty)
            print("Servo at 90° (DOWN)")

    def cleanup(self):
        self.servo.deinit()

