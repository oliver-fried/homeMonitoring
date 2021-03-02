#!/usr/bin/env python


import RPi.GPIO as GPIO
import time
import smtplib
import json

#getting data from JSON file
with open('/home/pi/src/homeMonitoring/monitoringParameters.json') as f:
    data = json.load(f)
airIntakePin = data['airIntakePin']
#setting up GPIO outputs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(airIntakePin, GPIO.OUT)



def airIntakeControl():
    
    GPIO.output(airIntakePin, 1)
    time.sleep(data["airIntakePinHighTimeInSeconds"])
    GPIO.output(airIntakePin, 0)



airIntakeControl()
GPIO.cleanup()