import os
import glob
import time
import RPi.GPIO as GPIO           # import RPi.GPIO module  
GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD 
GPIO.setup(24, GPIO.OUT) # set a port/pin as an output   



#initialize the device
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
print(base_dir)

maxTemp = 65
maxSlope = 20

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


def updateText():
    thermOneTemp.set(read_thermOnetemp())
    thermTwoTemp.set(read_thermTwotemp())
    timeTitle.set(time.ctime())
    text.after(1000, updateText)


def alarmTrigger(lastTemp):
    read_thermOnetemp_raw()
    read_thermOnetemp()
    if thermOnetemp_c >= maxTemp:
        if abs((thermOnetemp_c - lastTemp)/5) >= maxSlope:
            alarmTrigger(lastTemp)
        else:
            GPIO.output(24, 1)
    else:
        GPIO.output(24, 0)
        alarmTrigger(thermOnetemp_c)


alarmTrigger(22)