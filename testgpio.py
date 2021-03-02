import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT)
while 1<2:
    GPIO.output(15, 0)

GPIO.cleanup()
