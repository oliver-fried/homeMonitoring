#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import smtplib
import json

#getting data from JSON file
with open('/home/pi/src/homeMonitoring/monitoringParameters.json') as f:
    data = json.load(f)
alarmPin = data['alarmPin']
#setting up GPIO outputs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(alarmPin, GPIO.OUT)



def activateAlarm():
    
    GPIO.output(alarmPin, 1)
    time.sleep(3)
    GPIO.output(alarmPin,0)
    print("done")



activateAlarm()
GPIO.cleanup()

