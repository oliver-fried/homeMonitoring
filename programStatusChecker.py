#!/usr/bin/env python

#This program checks if policeSiren.py is running.
#Before running, make sure the presets in the 'parameters.json' file are correct
#May 2021, Oliver Fried, oliverfried3@gmail.com
f = open("programStatusStorage.txt", "r")
programStatus = float(f.read())

import time
import json
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
    
#setting up GPIO outputs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(data["policeSirenPin"], GPIO.OUT)

#getting data
alarmRunTimeInSeconds = data["alarmRunTimeInSeconds"]
alarmOffTimeInSeconds = data["alarmOffTimeInSeconds"]
policeSirenPin = data["policeSirenPin"]

#system check
print bcolors.OKBLUE + "System Check"

if alarmRunTimeInSeconds > 0 and alarmRunTimeInSeconds < 1800 and alarmRunTimeInSeconds != None:
    print bcolors.OKGREEN + "alarmRunTimeInSeconds OK"
else:
    print bcolors.FAIL + "alarmRunTimeInSeconds Variable ERROR"

if alarmOffTimeInSeconds > 0 and alarmOffTimeInSeconds < 1800 and alarmOffTimeInSeconds != None:
    print bcolors.OKGREEN + "alarmOffTimeInSeconds OK"
else:
    print bcolors.FAIL + "alarmOffTimeInSeconds Variable ERROR"

if policeSirenPin >=1 and policeSirenPin < 50 and policeSirenPin != None:
    print bcolors.OKGREEN + "policeSirenPin OK" +bcolors.ENDC
else:
    print bcolors.FAIL + "policeSirenPin Variable ERROR" + bcolors.ENDC

 





if programStatus == None:
    print "ERROR: INITIATE policeSiren.py BEFORE RUNNING THIS PROGRAM"
    exit()

elif programStatus != None:
    while True:
        f = open("programStatusStorage.txt", "r")
        print(f.read())
        if programStatus == "EXIT":
            print "ERROR: INITIATE policeSiren.py BEFORE RUNNING THIS PROGRAM"
            exit()
        else:
            programStatus = float(f.read())
            if programStatus < (time.time()-10):
                while programStatus < time.time()-10:
                    timeEnd = time.time() + alarmRunTimeInSeconds
                    
                    print "policeSiren.py is down!"
                    while time.time() < timeEnd:
                        GPIO.output(policeSirenPin, 1)
                        
                    timeOff = time.time() + alarmOffTimeInSeconds
                    while time.time() < timeOff:
                        GPIO.output(policeSirenPin, 0)
