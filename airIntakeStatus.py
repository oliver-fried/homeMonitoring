#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import smtplib
import json

def prelimFunctions():
    #getting data from JSON file
    with open('/home/pi/src/homeMonitoring/monitoringParameters.json') as f:
        data = json.load(f)

    airIntakeStatusPin = data['airIntakeStatusPin']
    #setting up GPIO outputs
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(airIntakeStatusPin, GPIO.IN)
    status = GPIO.input(airIntakeStatusPin)

    status = GPIO.input(airIntakeStatusPin)
    GPIO.cleanup()
    return status

def runProgram(statusVar):
    if statusVar == 1:
        print("Closed")  
    else:
        print("Open")


