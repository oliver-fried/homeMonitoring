#!/usr/bin/env python

#This program rings an alarm if the furnace temp gets too high.
#Before running, make sure the presets in the 'parameters.json' file are correct
#June 2020, Oliver Fried, oliverfried3@gmail.com

import os
import glob
import time
import RPi.GPIO as GPIO
import json
import smtplib
from datetime import datetime
import sys


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
    
print bcolors.FAIL + "**NOTE**: REMEMBER TO START programStatusChecker.py" +bcolors.ENDC

#getting data from JSON file
with open('monitoringParameters.json') as f:
    data = json.load(f)



#setting up GPIO outputs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(data["policeSirenPin"], GPIO.OUT)

#initialize the device
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#setup therm location
base_dir = '/sys/bus/w1/devices/'

#defining variables from JSON file
maxTemp = ((data["maxTempF"]- 32)*(0.55555555555555))
thermSerialNumber = data["furnaceThermometerSerialNumber"]
secondsBeforeUpdatingRate = data["secondsBeforeUpdatingRate"]
alarmRunTimeInSeconds = data["alarmRunTimeInSeconds"]
alarmOffTimeInSeconds = data["alarmOffTimeInSeconds"]
policeSirenPin = data["policeSirenPin"]


#getting the therm file
thermOneFolder = glob.glob(base_dir + thermSerialNumber)[0]
deviceOne_file = thermOneFolder + '/w1_slave'

#tracking the amount of time thermometers have been faulty
timeFaulty = []

#getting the temp from the output
def read_thermOnetemp():
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
        thermOnetemp_c = float(temp_string) / 1000.0
        return thermOnetemp_c


#setting up email sending
sender_email ='greenridgehomemonitoring@gmail.com'
rec_email = data['receivingEmail']
password = '1426Greenridge'
message = "WARNING! PLENUM IS TOO HOT!"

#I have this "try+ accept" code here because I want to try to get email connected, but if no internet, program will still run
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
except:
    print "-------------------"
    print "ERROR: No network connection, email function unavailable"


#main function
def alarmTrigger():
    #set the 
    GPIO.output(policeSirenPin, 0)
    timeFaulty = []
    
    try:
        f = open("programStatusStorage.txt", "w")
        f.write(str(time.time()) + "/" + str(read_thermOnetemp()))
        f.close()
    
        
        #if the therm shows a temp that is too high:
        if read_thermOnetemp() >= maxTemp:
            try:
                server.sendmail(sender_email, rec_email, message)
            except:
                print "-------------------"
            print("TOO HOT! (" + str((read_thermOnetemp() * 1.8 +32)) + " F)")

            while read_thermOnetemp() >= maxTemp:
                timeEnd = time.time() + alarmRunTimeInSeconds
                
                print "Temp is too high (" + str((read_thermOnetemp() * 1.8 +32)) + " F), waiting for it to lower"
                while time.time() < timeEnd:
                    GPIO.output(policeSirenPin, 1)
                    
                timeOff = time.time() + alarmOffTimeInSeconds
                while time.time() < timeOff:
                    GPIO.output(policeSirenPin, 0)
                    print "low"
            
        #if the temp isnt too high, wait a second and go get a new temp           
        else:
            print(bcolors.OKGREEN + "policeSiren.py:  Safe Temperature (" + str((read_thermOnetemp() * 1.8 +32)) + " F)" +bcolors.ENDC)
    except:
        print "ERROR: ISSUE READING TEMP! CHECK SYSTEM"
        timeFaulty.append(1)
        if len(timeFaulty)*secondsBeforeUpdatingRate >= 300:
            try:
                server.sendmail(sender_email, rec_email, "ERROR: ISSUE READING TEMP! CHECK SYSTEM")
            except:
                print "-------------------"

            timeEnd = time.time() + alarmRunTimeInSeconds
            while time.time() < timeEnd:
                GPIO.output(policeSirenPin, 1)
                    
            timeOff = time.time() + alarmOffTimeInSeconds
            while time.time() < timeOff:
                GPIO.output(policeSirenPin, 0)


#run the main program
try:
    while True:
        alarmTrigger()
        time.sleep(secondsBeforeUpdatingRate)

#this cleans up after using GPIO pins
except KeyboardInterrupt:
    GPIO.cleanup()
    f = open("programStatusStorage.txt", "w")
    f.write("EXIT")
    f.close()
    


