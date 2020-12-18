#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import smtplib
import json

def mainFunctions():
    #getting data from JSON file
    with open('monitoringParameters.json') as f:
        data = json.load(f)

    airIntakeStatusPin = data['airIntakeStatusPin']
    #setting up GPIO outputs
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(airIntakeStatusPin, GPIO.IN)
    status = GPIO.input(airIntakeStatusPin)

    status = GPIO.input(airIntakeStatusPin)
    GPIO.cleanup()
    return status            

mainFunctions()


