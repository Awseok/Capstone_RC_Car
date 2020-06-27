import RPi.GPIO as GPIO
from time import sleep

speed = 30

pin1 = 0
pin2 = 5

pin3 = 6
pin4 = 13

pin5 = 19
pin6 = 26

pin7 = 20
pin8 = 21

GPIO.setmode(GPIO.BCM)

GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)

GPIO.setup(pin3, GPIO.OUT)
GPIO.setup(pin4, GPIO.OUT)

GPIO.setup(pin5, GPIO.OUT)
GPIO.setup(pin6, GPIO.OUT)

GPIO.setup(pin7, GPIO.OUT)
GPIO.setup(pin8, GPIO.OUT)

pwm5 = GPIO.PWM(pin1, 100)
pwm6 = GPIO.PWM(pin2, 100)

pwm7 = GPIO.PWM(pin3, 100)
pwm8 = GPIO.PWM(pin4, 100)

pwm1 = GPIO.PWM(pin5, 100)
pwm2 = GPIO.PWM(pin6, 100)

pwm3 = GPIO.PWM(pin7, 100)
pwm4 = GPIO.PWM(pin8, 100)

pwm1.start(0)
pwm2.start(0)
pwm3.start(0)
pwm4.start(0)
pwm5.start(0)
pwm6.start(0)
pwm7.start(0)
pwm8.start(0)

#left-foward
pwm1.ChangeDutyCycle(0)
pwm2.ChangeDutyCycle(0)
pwm3.ChangeDutyCycle(speed)
pwm4.ChangeDutyCycle(0)
pwm5.ChangeDutyCycle(speed)
pwm6.ChangeDutyCycle(0)
pwm7.ChangeDutyCycle(0)
pwm8.ChangeDutyCycle(0)

sleep(1)

#right-back
pwm1.ChangeDutyCycle(0)
pwm2.ChangeDutyCycle(0)
pwm3.ChangeDutyCycle(0)
pwm4.ChangeDutyCycle(speed)
pwm5.ChangeDutyCycle(0)
pwm6.ChangeDutyCycle(speed)
pwm7.ChangeDutyCycle(0)
pwm8.ChangeDutyCycle(0)

sleep(1)

#foward
pwm1.ChangeDutyCycle(speed)
pwm2.ChangeDutyCycle(0)
pwm3.ChangeDutyCycle(speed)
pwm4.ChangeDutyCycle(0)
pwm5.ChangeDutyCycle(speed)
pwm6.ChangeDutyCycle(0)
pwm7.ChangeDutyCycle(speed)
pwm8.ChangeDutyCycle(0)

sleep(1)

#back
pwm1.ChangeDutyCycle(0)
pwm2.ChangeDutyCycle(speed)
pwm3.ChangeDutyCycle(0)
pwm4.ChangeDutyCycle(speed)
pwm5.ChangeDutyCycle(0)
pwm6.ChangeDutyCycle(speed)
pwm7.ChangeDutyCycle(0)
pwm8.ChangeDutyCycle(speed)

sleep(1)

#right-foward
pwm1.ChangeDutyCycle(speed)
pwm2.ChangeDutyCycle(0)
pwm3.ChangeDutyCycle(0)
pwm4.ChangeDutyCycle(0)
pwm5.ChangeDutyCycle(0)
pwm6.ChangeDutyCycle(0)
pwm7.ChangeDutyCycle(speed)
pwm8.ChangeDutyCycle(0)

sleep(1)

#left-back
pwm1.ChangeDutyCycle(0)
pwm2.ChangeDutyCycle(speed)
pwm3.ChangeDutyCycle(0)
pwm4.ChangeDutyCycle(0)
pwm5.ChangeDutyCycle(0)
pwm6.ChangeDutyCycle(0)
pwm7.ChangeDutyCycle(0)
pwm8.ChangeDutyCycle(speed)

sleep(1)

#left
pwm1.ChangeDutyCycle(0)
pwm2.ChangeDutyCycle(speed)
pwm3.ChangeDutyCycle(speed)
pwm4.ChangeDutyCycle(0)
pwm5.ChangeDutyCycle(speed)
pwm6.ChangeDutyCycle(0)
pwm7.ChangeDutyCycle(0)
pwm8.ChangeDutyCycle(speed)

sleep(1)

#right
pwm1.ChangeDutyCycle(speed)
pwm2.ChangeDutyCycle(0)
pwm3.ChangeDutyCycle(0)
pwm4.ChangeDutyCycle(speed)
pwm5.ChangeDutyCycle(0)
pwm6.ChangeDutyCycle(speed)
pwm7.ChangeDutyCycle(speed)
pwm8.ChangeDutyCycle(0)

sleep(1)

#u-turn
pwm1.ChangeDutyCycle(speed)
pwm2.ChangeDutyCycle(0)
pwm3.ChangeDutyCycle(0)
pwm4.ChangeDutyCycle(speed)
pwm5.ChangeDutyCycle(speed)
pwm6.ChangeDutyCycle(0)
pwm7.ChangeDutyCycle(0)
pwm8.ChangeDutyCycle(speed)

sleep(3)

pwm1.stop()
pwm2.stop()
pwm3.stop()
pwm4.stop()
pwm5.stop()
pwm6.stop()
pwm7.stop()
pwm8.stop()

GPIO.cleanup()