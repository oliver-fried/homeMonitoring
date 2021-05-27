#!/usr/bin/env python


#CHANGE THE LOCATION OF JSON ON LINE 14
#This program returns the temp of the outside. It is used for the website.
#Before running, make sure the presets in the 'monitoringParameters.json' file are correct
#June 2020, Oliver Fried, oliverfried3@gmail.com

import os
import glob
import json
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
    
    
#assigning value to varibles
softAlarmPin = data["softAlarmPin"]
alarmRunTimeInSeconds = data["alarmRunTimeInSeconds"]
alarmOffTimeInSeconds = data["alarmOffTimeInSeconds"]
secondsBeforeUpdatingRate = data["secondsBeforeUpdatingRate"]

#setting up GPIO outputs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(softAlarmPin, GPIO.OUT)

#initialize the device
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#setup therm location
base_dir = '/sys/bus/w1/devices/'


#########################################################
#                    outside temp data
#defining variables from JSON file
outsideThermSerialNumber = data["outsideThermometerSerialNumber"]
insideThermSerialNumber = data["houseThermometerSerialNumber"]

#getting the temp from the output
def read_thermOnetemp(serialNumber):
    
    thermOneFolder = glob.glob(base_dir + serialNumber)[0]
    deviceOne_file = thermOneFolder + '/w1_slave'

    f=open(deviceOne_file, 'r')
    thermOnelines = f.readlines()
    f.close()
    #once in a while it throws an error. this gets a new temp if error is thrown
    while thermOnelines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        f=open(deviceOne_file, 'r')
        thermOnelines = f.readlines()
        f.close()
    equals_pos = thermOnelines[1].find('t=')
    #if output looks fine, do this:
    if equals_pos != -1:
        temp_string = thermOnelines[1][equals_pos+2:]
        thermOnetemp_c = round(1.8*(float(temp_string) / 1000.0) +32, 2)
        return thermOnetemp_c
    
    



#this alerts us to whether one should close or open the windows during the summer
#by comparing inside and outside temperatures

aboveLastIteration = None
while True:
    houseTemp = read_thermOnetemp(insideThermSerialNumber)
    outsideTemp = read_thermOnetemp(outsideThermSerialNumber)
    
    if outsideTemp > houseTemp:
    
        if aboveLastIteration == False:
        
            f=open("softAlarmNotificationTracker.txt", "a")
            f.write("It's warmer outside than inside/")
            f.close()
            print "temp outside is warmer than inside"
            GPIO.output(softAlarmPin, 1)
            time.sleep(10)
            GPIO.output(softAlarmPin, 0)
            print "waiting a half hour to continue..."

            time.sleep(1800)
        aboveLastIteration = True
        
    if outsideTemp < houseTemp:
        
        if aboveLastIteration == True:
    
            f=open("softAlarmNotificationTracker.txt", "a")
            f.write("It's cooler outside than inside/")
            f.close()
            print "temp outside is cooler than inside"
            GPIO.output(softAlarmPin, 1)
            time.sleep(10)
            GPIO.output(softAlarmPin, 0)
            print "waiting a half hour to continue..."
            time.sleep(1800)
        aboveLastIteration = False
    print bcolors.OKGREEN + "outsideDataMonitor.py:  Monitoring (In: " + str(houseTemp) +"/Out: "+ str(outsideTemp) + "above last iteration? " + str(aboveLastIteration) + ")" + bcolors.ENDC 
    time.sleep(1)
        
        
        
        
        
        
        

