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

#getting data from JSON file
with open('parameters.json') as f:
    data = json.load(f)

#setting up GPIO outputs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(data["alarmPin"], GPIO.OUT)

#initialize the device
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#setup therm location
base_dir = '/sys/bus/w1/devices/'

#defining variables from JSON file
maxTemp = data["maxTempC"]
maxSlope = data["maxSlopeC"]
thermSerialNumber = data["furnaceThermometerSerialNumber"]
secondsBeforeUpdatingRate = data["secondsBeforeUpdatingRate"]

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
def read_thermOnetemp():
    thermOnelines = read_thermOnetemp_raw()
    #once in a while it throws an error. this gets a new temp if error is thrown
    while thermOnelines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        thermOnelines = read_thermOnetemp_raw()
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
message = "Plenum is too hot!"
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, password)




#main function
def alarmTrigger(lastTemp):
    read_thermOnetemp_raw()
    
    #if the therm shows a temp that is too high:
    if read_thermOnetemp() >= maxTemp:
        #if the slope is too large, its an error and we need to get a new data point
        if abs((read_thermOnetemp() - lastTemp)/1) >= maxSlope:
            print("Extraneous temp, disregard")
            alarmTrigger(lastTemp)

        #otherwise, RING THE ALARM!!!    
        else:
            server.sendmail(sender_email,rec_email, message)
            while True:
                GPIO.output(data['alarmPin'], 1)
                print("TOO HOT!")

    #if the temp isnt too high, wait a second and go get a new temp           
    else:
        GPIO.output(data['alarmPin'], 0)
        print("Safe Temperature")
        time.sleep(secondsBeforeUpdatingRate)
        alarmTrigger(read_thermOnetemp())
        

#un the main program
alarmTrigger(23)

#this cleans up after using GPIO pins
GPIO.cleanup()