#-*- coding: utf-8 -*-
import RPi.GPIO as GPIO, sys, socket, threading, time


#thread lock value
lock = threading.Lock()

'''
exit flag
closeFlag is connection_check_value in thread
isClose is program exit flag
'''
isClose = False
closeFlag = False

#thread - check that client socket connection is alive
def checkConnect(intervalValue):
    
    interval = intervalValue
    global isClose
    global closeFlag
    
    '''
    Every [interval] seconds, server send connect_check_character 'C'
    '''
    while True:
        #current execute time
        startTime = time.perf_counter()
            
        checkMsg = "C"
        
        print("alive check")
                
        '''
        wait [interval] seconds
        for client send return value 'C'
        ''' 
        
        while True:
            #resourse lock
            lock.acquire()
            
            #send to connection socket 'c'
            connectCheck = connectionSocket.send(checkMsg.encode('utf-8'))
            
            #connectCheck is accpet send msg byte, if not 1 is closed
            if connectCheck != 1:
                print("socket closed")
                isClose = True
            
            #recv 'c' in 30 seconds
            closeFlag = True
            
            lock.release()
        
            while time.perf_counter() - startTime < interval:
                pass
            
            lock.acquire()
            
            if closeFlag:
                isClose = True
                
            lock.release()
            
            break
        
def waitTime(endTime):
    startTime = time.perf_counter()
    while time.perf_counter() - startTime < endTime:
        pass

#pin output value
HIGH = 1
LOW = 0

#pwm setting(speed, degree, pin)
#speed : 0 ~ 250?
servoDegree = 90
motorSpeed = 50
servoMotorPwmPin = 13
motorPwmPin = 12
motorPin = [20,21]

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
servoPwm.start(servoDegree)    

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
    
    #connectio check thread
    checkCycle = 30
    connectionTread = threading.Thread(target=checkConnect, args=(checkCycle,), daemon=True)
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
            servoPwm.stop()
            motorPwm.stop()
            GPIO.cleanup()
            sys.exit()
            
        cntlMsg = cntlMsg.decode('utf-8')
       
        #close
        if cntlMsg == 'E':
            isClose = True
        elif cntlMsg == 'C':
            closeFlag = False
        #newline charator
        elif cntlMsg =='\n':
            continue
        #foward
        elif cntlMsg == 'F':
            cntlFlag = [HIGH, LOW]
        #rear
        elif cntlMsg == 'R':
            cntlFlag = [LOW, HIGH]
        #break
        elif cntlMsg == 'B':
            cntlFlag = [LOW, LOW]
        #Nuetral
        elif cntlMsg == 'L':
            servoDegree = servoDegree - 3
        #Back
        elif cntlMsg == 'R':
            servoDegree = servoDegree + 3
        #speed value
        elif cntlMsg.isdecimal():               
            motor1speed = int(cntlMsg) * 10
        #exception
        else:
            print(cntlMsg + "is garbage")
        
        #change servo degree
        
        if(servoDegree < 30):
            servoDegree = 30
        elif(servoDegree > 120):
            servoDegree = 120
            
        servoPwm.ChangeDutyCycle(servoDegree)
        
        GPIO.output(motorPin[0], cntlFlag[0])
        GPIO.output(motorPin[1], cntlFlag[1])
     
    
