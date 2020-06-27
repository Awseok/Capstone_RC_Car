#-*- coding: utf-8 -*-
import RPi.GPIO as GPIO, sys, socket, threading, time

'''
exit flag
closeFlag is connection_check_value in thread
isClose is program exit flag
'''
isClose = False
closeFlag = False

#pin output value
HIGH = 1
LOW = 0

#pwm setting(speed, degree, pin)
#speed : 0 ~ 250?
servoDegree = 50
motorSpeed = 50
servoMotorPwmPin = 13
motorPwmPin = 12
motorPin = [20,21]
SERVO_MAX_DUTY = 11
SERVO_MIN_DUTY = 4

#GPIO initialize
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#GPIO setting
GPIO.setup(motorPin[0], GPIO.OUT)
GPIO.setup(motorPin[1], GPIO.OUT)

#GPIO first value
GPIO.output(motorPin[0], LOW)
GPIO.output(motorPin[1], LOW)

#GPIO pwm pin setting
GPIO.setup(motorPwmPin, GPIO.OUT)
GPIO.setup(servoMotorPwmPin, GPIO.OUT)

#pwm bind
motorPwm = GPIO.PWM(motorPwmPin, motorSpeed)
servoPwm = GPIO.PWM(servoMotorPwmPin, servoDegree)

#pwm start
motorPwm.start(motorSpeed)
servoPwm.start(0)    
   
while True:
    inst = input("degree: time: f/b: ")
        
    #motor output flag (motor1 in1, motor1 in2, motor2 in1, motor2 in2)
    cntlFlag = [LOW, LOW]
        

    servoDegree = int(inst.split()[0])
    
    if(servoDegree == -1):
        isClose = True
        
    #close
    if isClose:
        servoPwm.stop()
        motorPwm.stop()
        GPIO.cleanup()
        sys.exit()

    doTime = int(inst.split()[1])

    if(inst.split()[2] == 'F'):
        cntlFlag = [HIGH, LOW]
    else:
        cntlFlag = [LOW, HIGH]
        
    #change servo degree
        
    if(servoDegree < 0):
        servoDegree = 0
    elif(servoDegree > 180):
        servoDegree = 180
        
    duty = SERVO_MIN_DUTY+(servoDegree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
    servoPwm.ChangeDutyCycle(duty)
        
    GPIO.output(motorPin[0], cntlFlag[0])
    GPIO.output(motorPin[1], cntlFlag[1])


    time.sleep(doTime)

    GPIO.output(motorPin[0], LOW)
    GPIO.output(motorPin[1], LOW)


