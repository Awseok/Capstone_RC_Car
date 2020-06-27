import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

pwmPin1 = 5
pwmPin2 = 6

pin1 = 20
pin2 = 21
pin3 = 19
pin4 = 26

GPIO.setup(pwmPin1, GPIO.OUT)
GPIO.setup(pwmPin2, GPIO.OUT)
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(pin3, GPIO.OUT)
GPIO.setup(pin4, GPIO.OUT)

freq = 70

pwm1 = GPIO.PWM(pwmPin1, freq)
pwm2 = GPIO.PWM(pwmPin2, freq)

left_up = 0.75
left_rev = 2.5
left_down = (left_rev - left_up) / 2 + left_up

right_up = 2.5
right_rev = 0.75
right_down = (right_up - right_rev) / 2 + right_rev

positionlistleft = [left_up, left_down]
positionlistright = [right_up, right_down]

mpc_left = 1000 / freq

pwm1.start(freq)

for i in range(3):
    for positionleft in positionlistleft:
        dcpleft = positionleft * 100 / mpc_left
        pwm1.ChangeDutyCycle(dcpleft)
        time.sleep(1)
        
pwm1.stop()

GPIO.cleanup()