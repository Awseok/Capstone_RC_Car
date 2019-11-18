#-*- coding: utf-8 -*-
"""
Created on Sat Nov 16 15:05:25 2019

@author: wonseok

need test
"""

import RPi.GPIO as GPIO, sys, socket, threading, time

#recive message(global)
cntlMsg = ''
lock = threading.Lock()

#flag for close
isClose = False

#thread - check that client socket connection is alive
def checkConnect(intervalValue):
    interval = intervalValue
    global isClose
    '''
    Every [interval] second, server send connect check value 'C'
    '''
    while True:
        #current execute time
        startTime = time.perf_counter()
            
        checkMsg = "C"
        
        print("alive check")
        #client socket send closed
        
        '''
        wait [interval] second
        for client send return value 'C'
        ''' 
        checkTime = time.perf_counter()
        while True:
            lock.acquire()
            connectCheck = connectionSocket.send(checkMsg.encode('utf-8'))
            if connectCheck != 1:
                print("socket closed")
                isClose = True
            
            lock.release()
            while time.perf_counter() - startTime < interval:
                pass
        
def waitTime(endTime):
    startTime = time.perf_counter()
    while time.perf_counter() - startTime < endTime:
        pass

#pin output value
HIGH = 1
LOW = 0

#pwm setting(speed, pin)
motor1speed = 50
motor2speed = 50
leftMotor = [19,26]
rightMotor = [20,21]
enableButton = [6, 12]

#GPIO motor pin setting
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(leftMotor[0], GPIO.OUT)
GPIO.setup(leftMotor[1], GPIO.OUT)
GPIO.setup(rightMotor[0], GPIO.OUT)
GPIO.setup(rightMotor[1], GPIO.OUT)

#GPIO first value
GPIO.output(leftMotor[0], LOW)
GPIO.output(leftMotor[1], LOW)
GPIO.output(rightMotor[0], LOW)
GPIO.output(rightMotor[1], LOW)

#GPIO pwm pin setting
GPIO.setup(enableButton[0], GPIO.OUT)
GPIO.setup(enableButton[1], GPIO.OUT)

#pwm bind
pwm1 = GPIO.PWM(enableButton[0], motor1speed)
pwm2 = GPIO.PWM(enableButton[1], motor2speed)

#pwm start
pwm1.start(motor1speed)
pwm2.start(motor2speed)    

#ip, port
#ip = input("ip: ")
ip = '192.168.43.250'

#port = input("port: ")
port = 54321
        
addr = (ip, int(port))
 
print("ip, port :" + ip + ", ", port)

#bind Server socket
while True:
    while True:
        try:
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Make server socket")
        
            serverSocket.bind(addr)
            print("binded socket")
            break
    
        except:
            print("reconnect")
            serverSocket.close()
            waitTime(10)
            continue
    
    #waiting for client socket(1)    
    serverSocket.listen(1)
    
    #get client socket
    connectionSocket, connectAddr = serverSocket.accept();
           
    print("connect")   
    
    connectionTread = threading.Thread(target=checkConnect, args=(30,), daemon=True)
    connectionTread.start()
    
    #comunication    
    while True:
                
        #motor output flag (motor1 in1, motor1 in2, motor2 in1, motor2 in2)
        cntlFlag = [LOW, LOW, LOW, LOW]
        
        #recive
        try:
            cntlMsg = connectionSocket.recv(1)
            
        #can't handle IOException
        except:
            isClose = True
            
        finally:
            #if client send socket close
            if cntlMsg == b'':
                isClose = True
            
            #socket error
            elif cntlMsg == -1:
                isClose = True
                
        #close
        if isClose:
            connectionSocket.close()
            serverSocket.close()
            pwm1.stop()
            pwm2.stop()
            GPIO.cleanup()
            sys.exit()
            
        cntlMsg = cntlMsg.decode('utf-8')
       
        #close
        if cntlMsg == 'E':
            isClose = True
        #newline charator
        elif cntlMsg =='\n':
            continue
        #left
        elif cntlMsg == 'L':
            cntlFlag = [LOW, LOW, HIGH, LOW]
        #Right
        elif cntlMsg == 'R':
            cntlFlag = [HIGH, LOW, LOW, LOW]
        #Foward
        elif cntlMsg == 'F':
            cntlFlag = [HIGH, LOW, HIGH, LOW]
        #Nuetral
        elif cntlMsg == 'N':
            cntlFlag = [LOW, LOW, LOW, LOW]
        #Back
        elif cntlMsg == 'B':
            cntlFlag = [LOW, HIGH, LOW, HIGH]
        #speed value
        elif cntlMsg.isdecimal():               
            motor1speed = int(cntlMsg) * 10
            motor2speed = int(cntlMsg) * 10
        #exception
        else:
            print(cntlMsg + "is garbage")
        
        #change motor speed
        pwm1.ChangeDutyCycle(motor1speed)
        pwm2.ChangeDutyCycle(motor2speed)
        
        #motor[in1, in2]
        leftMotorFlag = cntlFlag[0:2]
        rightMotorFlag = cntlFlag[2:4]    

        GPIO.output(leftMotor[0], leftMotorFlag[0])
        GPIO.output(leftMotor[1], leftMotorFlag[1])
        GPIO.output(rightMotor[0], rightMotorFlag[0])
        GPIO.output(rightMotor[1], rightMotorFlag[1])
    
