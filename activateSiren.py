'''import RPi.GPIO as GPIO'''
import time

#setting up GPIO outputs
'''GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)

def activateSiren():
    GPIO.output(18, 1)
    time.sleep(3)
    GPIO.output(18,0)


#activateSiren()
GPIO.cleanup()'''

def returnHello():
    return "hello"

print(returnHello())