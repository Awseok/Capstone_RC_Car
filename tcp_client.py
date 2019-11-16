from socket import *
from time import sleep
import RPi.GPIO as GPIO

HIGH = 1
LOW = 0

leftMotar = [19,26]
rightMotar = [20,21]
enableButton = [6, 12]

GPIO.setwarnings(LOW)
GPIO.setmode(GPIO.BCM)
GPIO.setup(leftMotar[0], GPIO.OUT)
GPIO.setup(leftMotar[1], GPIO.OUT)
GPIO.setup(rightMotar[0], GPIO.OUT)
GPIO.setup(rightMotar[1], GPIO.OUT)

GPIO.output(leftMotar[0], LOW)
GPIO.output(leftMotar[1], LOW)
GPIO.output(rightMotar[0], LOW)
GPIO.output(rightMotar[1], LOW)

GPIO.setup(enableButton[0], GPIO.OUT)
GPIO.setup(enableButton[1], GPIO.OUT)

cnt1 = 50
cnt2 = 50

pwm1 = GPIO.PWM(enableButton[0], cnt1)
pwm2 = GPIO.PWM(enableButton[1], cnt2)

pwm1.start(cnt1)
pwm2.start(cnt2)

ip = '192.168.43.249'

port = 43567

addr = (ip,port)

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(addr)
serverSocket.listen(1)
connectionSocket, conectAddr = serverSocket.accept();
print("connect")

try:
    while True:
        cntlFlag = [LOW, LOW, LOW, LOW]
        cntlMsg = connectionSocket.recv(1)
        cntlMsg = cntlMsg.decode('utf-8')
        
        print(cntlMsg)

        if cntlMsg == 'L':
            cntlFlag = [LOW, LOW, HIGH, LOW]
        elif cntlMsg == 'R':
            cntlFlag = [HIGH, LOW, LOW, LOW]
        elif cntlMsg == 'F':
            cntlFlag = [HIGH, LOW, HIGH, LOW]
        elif cntlMsg == 'N':
            cntlFlag = [LOW, LOW, LOW, LOW]
        elif cntlMsg == 'B':
            cntlFlag = [LOW, HIGH, LOW, HIGH]
        else:
            continue
                
        leftMotarFlag = cntlFlag[0:2]
        rightMotarFlag = cntlFlag[2:4]    
    
        '''
        speed change = pwm1.changeDutyCycle(speed)
        '''
        
        GPIO.output(leftMotar[0], leftMotarFlag[0])
        GPIO.output(leftMotar[1], leftMotarFlag[1])
        GPIO.output(rightMotar[0], rightMotarFlag[0])
        GPIO.output(rightMotar[1], rightMotarFlag[1])
   
        
        cntlFlag = []
    
except KeyboardInterrupt:
    pwm1.stop()
    GPIO.cleanup()
    sys.exit()
    
    
