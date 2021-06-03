#!/usr/bin/env python

#This program checks if policeSiren.py is running.
#Before running, make sure the presets in the 'parameters.json' file are correct
#May 2021, Oliver Fried, oliverfried3@gmail.com


import time
import json
import RPi.GPIO as GPIO
GPIO.setwarnings(False)



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
    print bcolors.OKGREEN + "alarmRunTimeInSeconds   OK"
else:
    print bcolors.FAIL + "alarmRunTimeInSeconds Variable ERROR"
    exit()
    
if alarmOffTimeInSeconds > 0 and alarmOffTimeInSeconds < 1800 and alarmOffTimeInSeconds != None:
    print bcolors.OKGREEN + "alarmOffTimeInSeconds   OK"
else:
    print bcolors.FAIL + "alarmOffTimeInSeconds Variable ERROR"
    exit()

if policeSirenPin >=1 and policeSirenPin < 50 and policeSirenPin != None:
    print bcolors.OKGREEN + "policeSirenPin          OK" +bcolors.ENDC
else:
    print bcolors.FAIL + "policeSirenPin Variable ERROR" + bcolors.ENDC
    exit()

print "_____________________________________"
print "           Time(seconds) Temp (C)"
 


f = open("programStatusStorage.txt", "r")
programStatus = f.read()
f.close()


if programStatus == None:
    print "ERROR: INITIATE policeSiren.py BEFORE RUNNING THIS PROGRAM"
    exit()

elif programStatus != None:
    while True:
        f = open("programStatusStorage.txt", "r")
        data = f.read()
        f.close()
        if data == "EXIT":
            print "ERROR: INITIATE policeSiren.py BEFORE RUNNING THIS PROGRAM"
            exit()
        else:
            if data == "":
                time.sleep(1)
                f = open("programStatusStorage.txt", "r")
                data=f.read()
                f.close()
                if data == "EXIT":
                    print "ERROR: INITIATE policeSiren.py BEFORE RUNNING THIS PROGRAM"
                    exit()
            programStatus = float(data.split("/")[0])
            lastTemp = float(data.split("/")[1])
            if programStatus < (time.time()-10) or lastTemp < 0 or lastTemp > 93.3:
                while programStatus < time.time()-10:
                    
                    print "policeSiren.py is down!"
                    GPIO.output(policeSirenPin, 1)
                        
                    f = open("programStatusStorage.txt", "r")
                    data=f.read()
                    f.close()
                    programStatus = float(data)
                    
            else:
                print bcolors.OKGREEN + "Monitoring (" + str(data) + ")" +bcolors.ENDC
                time.sleep(1)
