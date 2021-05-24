import RPi.GPIO as GPIO
import time
import json

#getting data from JSON file
with open('monitoringParameters.json') as f:
        #define the data inside the JSON file as "data." This will allow me to access it later on when I define variables.
        data = json.load(f)

alarmPin = data["alarmPin"]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(alarmPin, GPIO.OUT)

def testPin():
    highEnd = time.time() + 5

    while time.time() < highEnd:
        GPIO.output(alarmPin, 1)
        print "high"

    lowEnd = time.time() + 5
    while time.time() < lowEnd:
        GPIO.output(alarmPin, 0)
        print "low"

while True:
    testPin()

