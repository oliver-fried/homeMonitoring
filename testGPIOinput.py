import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.IN)
while 1<2:
    print(GPIO.input(15))
    time.sleep(.5)
GPIO.cleanup()