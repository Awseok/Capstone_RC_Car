from socket import *
from time import sleep
import RPi.GPIO as GPIO, os, sys

def run():
    HIGH = 1
    LOW = 0
    cnt1 = 50
    cnt2 = 50
    close = False

    leftMotor = [19,26]
    rightMotor = [20,21]
    enableButton = [6, 12]
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(leftMotor[0], GPIO.OUT)
    GPIO.setup(leftMotor[1], GPIO.OUT)
    GPIO.setup(rightMotor[0], GPIO.OUT)
    GPIO.setup(rightMotor[1], GPIO.OUT)

    GPIO.output(leftMotor[0], LOW)
    GPIO.output(leftMotor[1], LOW)
    GPIO.output(rightMotor[0], LOW)
    GPIO.output(rightMotor[1], LOW)

    GPIO.setup(enableButton[0], GPIO.OUT)
    GPIO.setup(enableButton[1], GPIO.OUT)

    pwm1 = GPIO.PWM(enableButton[0], cnt1)
    pwm2 = GPIO.PWM(enableButton[1], cnt2)

    pwm1.start(cnt1)
    pwm2.start(cnt2)    

    ip = '192.168.43.249'
    #ip = input("ip: ")
        
    port = 54321
    #port = input("port: ")

    addr = (ip, int(port))

    serverSocket = socket(AF_INET, SOCK_STREAM)
    
    try:
        serverSocket.bind(addr)
    except:
        print("reconnect")
        sleep(2)
        serverSocket.close()
        os.execl(sys.executable, *sys.argv)
        
    serverSocket.listen(1)
    connectionSocket, connectAddr = serverSocket.accept();
    
    print("connect")

    while True:
        cntlFlag = [LOW, LOW, LOW, LOW]
        
        try:
            cntlMsg = connectionSocket.recv(1)
        except:
            close()
        finally:
            if cntlMsg == b'':
                close()
            elif cntlMsg == -1:
                close()
            
        cntlMsg = cntlMsg.decode('utf-8')
       
        if cntlMsg == 'E':
            close = True
        elif cntlMsg =='\n':
            continue
        elif cntlMsg == 'L':
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
            cnt1 = int(cntlMsg)
            cnt2 = int(cntlMsg)   
                                
        pwm1.ChangeDutyCycle(cnt1)
        pwm2.ChangeDutyCycle(cnt2)

        leftMotorFlag = cntlFlag[0:2]
        rightMotorFlag = cntlFlag[2:4]    

        GPIO.output(leftMotor[0], leftMotorFlag[0])
        GPIO.output(leftMotor[1], leftMotorFlag[1])
        GPIO.output(rightMotor[0], rightMotorFlag[0])
        GPIO.output(rightMotor[1], rightMotorFlag[1])


        if close == True:
            connectionSocket.close()
            serverSocket.close()
            pwm1.stop()
            pwm2.stop()
            GPIO.cleanup()
            sys.exit()
    
if __name__ == "__maiin__":    
    run()

run()
    

    