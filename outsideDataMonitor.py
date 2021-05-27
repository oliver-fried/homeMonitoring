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
thermSerialNumber = data["outsideThermometerSerialNumber"]

#getting the therm file
thermOneFolder = glob.glob(base_dir + thermSerialNumber)[0]
deviceOne_file = thermOneFolder + '/w1_slave'

#reading in the raw output
def read_thermOnetemp_raw():
    f=open(deviceOne_file, 'r')
    thermOnelines = f.readlines()
    f.close()
    return thermOnelines

#getting the temp from the output
def outsideRead_thermOnetemp():
    thermOnelines = read_thermOnetemp_raw()
    #once in a while it throws an error. this gets a new temp if error is thrown
    while thermOnelines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        thermOnelines = read_thermOnetemp_raw()
    equals_pos = thermOnelines[1].find('t=')
    #if output looks fine, do this:
    if equals_pos != -1:
        temp_string = thermOnelines[1][equals_pos+2:]
        outsideThermOnetemp_c = round(1.8*(float(temp_string) / 1000.0) +32, 2)
        return outsideThermOnetemp_c
    
#################################################################
    #inside temp data
    
thermSerialNumber = data["houseThermometerSerialNumber"]

#getting the therm file
thermOneFolder = glob.glob(base_dir + thermSerialNumber)[0]
deviceOne_file = thermOneFolder + '/w1_slave'

#reading in the raw output
def read_thermOnetemp_raw():
    f=open(deviceOne_file, 'r')
    thermOnelines = f.readlines()
    f.close()
    return thermOnelines

#getting the temp from the output
def houseRead_thermOnetemp():
    thermOnelines = read_thermOnetemp_raw()
    #once in a while it throws an error. this gets a new temp if error is thrown
    while thermOnelines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        thermOnelines = read_thermOnetemp_raw()
    equals_pos = thermOnelines[1].find('t=')
    #if output looks fine, do this:
    if equals_pos != -1:
        temp_string = thermOnelines[1][equals_pos+2:]
        houseThermOnetemp_c = round(1.8*(float(temp_string) / 1000.0) +32, 2)
        return houseThermOnetemp_c


#this alerts us to whether one should close or open the windows during the summer
#by comparing inside and outside temperatures

aboveLastIteration = None
belowLastIteration = None
while True:
    houseTemp = houseRead_thermOnetemp()
    outsideTemp = outsideRead_thermOnetemp()
    
    if outsideTemp > houseTemp:
    
        if aboveLastIteration == False:
        
            f=open("softAlarmNotificationTracker.txt", "a")
            f.write("It's warmer outside than inside/")
            f.close()
            print "temp outside is warmer than inside"
            for x in range(5):
                
                timeEnd = time.time() + alarmRunTimeInSeconds

                while time.time() < timeEnd:
                    GPIO.output(softAlarmPin, 1)

                timeOff = time.time() + alarmOffTimeInSeconds

                while time.time() < timeOff:
                    GPIO.output(softAlarmPin, 0)
                    
        aboveLastIteration = True
        belowLastIteration == False
        
    if outsideTemp < houseTemp:
        if belowLastIteration == False:
    
            f=open("softAlarmNotificationTracker.txt", "a")
            f.write("It's cooler outside than inside/")
            f.close()
            print "temp outside is cooler than inside"
            for x in range(5):
                
                timeEnd = time.time() + alarmRunTimeInSeconds

                while time.time() < timeEnd:
                    GPIO.output(softAlarmPin, 1)

                timeOff = time.time() + alarmOffTimeInSeconds

                while time.time() < timeOff:
                    GPIO.output(softAlarmPin, 0)
                    
        belowLastIteration = True
        aboveLastIteration == False
    print bcolors.OKGREEN + "Monitoring (" + str(time.time()) + ")" + bcolors.ENDC 
    time.sleep(1)
        
        
        
        
        
        
        

