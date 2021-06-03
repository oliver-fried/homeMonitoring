#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import json


def mainFunctions():
    #getting data from JSON file
    with open('/home/pi/TechnicalStuff/WorkingAlarmSystemCode/Code') as f:
        data = json.load(f)
    
    

    airIntakeStatusPin = data['airIntakeStatusPin']
    #setting up GPIO outputs
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(airIntakeStatusPin, GPIO.IN)

    status = GPIO.input(airIntakeStatusPin)
    
    return status

print mainFunctions()


GPIO.cleanup()