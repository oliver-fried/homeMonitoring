#!/usr/bin/env python

#This program checks if policeSiren.py is running.
#Before running, make sure the presets in the 'parameters.json' file are correct
#May 2021, Oliver Fried, oliverfried3@gmail.com
from policeSiren import programStatus
import time
import RPi.GPIO as GPIO

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#getting data from JSON file
with open('monitoringParameters.json') as f:
    data = json.load(f)

#getting data
alarmRunTimeInSeconds = data["alarmRunTimeInSeconds"]
alarmOffTimeInSeconds = data["alarmOffTimeInSeconds"]
policeSirenPin = data["policeSirenPin"]

#system check
print bcolors.OKBLUE + "System Check"

if alarmRunTimeInSeconds > 0 and < 1800 and != None:
    print bcolors.OKGREEN + "alarmRunTimeInSeconds OK"
else:
    print bcolors.FAIL + "alarmRunTimeInSeconds Variable ERROR"

if alarmOffTimeInSeconds > 0 and < 1800 and != None:
    print bcolors.OKGREEN + "alarmOffTimeInSeconds OK"
else:
    print bcolors.FAIL + "alarmOffTimeInSeconds Variable ERROR"

if policeSirenPin >=1 and < 50 and != None:
    print bcolors.OKGREEN + "policeSirenPin OK"
else:
    print bcolors.FAIL + "policeSirenPin Variable ERROR"

if alarmRunTimeInSeconds > 1 and < 1800 and 1= None:
    print bcolors.OKGREEN + "alarmRunTimeInSeconds OK"
else:
    print bcolors.FAIL + "alarmRunTimeInSeconds Variable ERROR"





if programStatus == None:
    print "ERROR: INITIATE policeSiren.py BEFORE RUNNING THIS PROGRAM"

elif programStatus != None:
    while True:
        if programStatus != (time.time()-30):
            while programStatus != time.time()-30:
                 timeEnd = time.time() + alarmRunTimeInSeconds
                
                print "policeSiren.py is down!"
                while time.time() < timeEnd:
                    GPIO.output(policeSirenPin, 1)
                    
                timeOff = time.time() + alarmOffTimeInSeconds
                while time.time() < timeOff:
                    GPIO.output(policeSirenPin, 0)
                    print "low"
