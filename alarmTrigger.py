#!/usr/bin/env python

import os
import glob
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT) 
#initialize the device
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
print(base_dir)

maxTemp = 65
maxSlope = 10

thermOneFolder = glob.glob(base_dir + '28*')[0]
deviceOne_file = thermOneFolder + '/w1_slave'


def read_thermOnetemp_raw():
    f=open(deviceOne_file, 'r')
    thermOnelines = f.readlines()
    f.close()
    return thermOnelines


def read_thermOnetemp():
    thermOnelines = read_thermOnetemp_raw()
    while thermOnelines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        thermOnelines = read_thermOnetemp_raw()
    equals_pos = thermOnelines[1].find('t=')
    if equals_pos != -1:
        temp_string = thermOnelines[1][equals_pos+2:]
        thermOnetemp_c = float(temp_string) / 1000.0
        return thermOnetemp_c





def alarmTrigger(lastTemp):
    read_thermOnetemp_raw()
    
    if read_thermOnetemp() >= maxTemp:
        if abs((read_thermOnetemp() - lastTemp)/1) >= maxSlope:
            print("Extraneous temp, disregard")
            alarmTrigger(lastTemp)
            
        else:
            while True:
                GPIO.output(18, 1)
                print("TOO HOT!")
    else:
        GPIO.output(18, 0)
        print("Safe Temperature")
        time.sleep(1)
        alarmTrigger(read_thermOnetemp())
        


alarmTrigger(23)

GPIO.cleanup()