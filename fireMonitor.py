import os
import glob
import time
import RPi.GPIO as GPIO
import json
import smtplib
import time
import RPi.GPIO as GPIO

#getting data from JSON file
with open('monitoringParameters.json') as f:
        data = json.load(f)

airIntakeStatusPin = data['airIntakeStatusPin']
alarmPin = data["alarmPin"]
#setting up GPIO outputs
GPIO.setmode(GPIO.BOARD)

GPIO.setup(airIntakeStatusPin, GPIO.IN)
GPIO.setup(alarmPin, GPIO.OUT)

#initialize the device
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#setup therm location
base_dir = '/sys/bus/w1/devices/'

#defining variables from JSON file
maxTemp = data["maxTempC"]
maxSlope = data["maxSlopeC"]
thermSerialNumber = data["furnaceThermometerSerialNumber"]

#getting the therm file
thermOneFolder = glob.glob(base_dir + thermSerialNumber)[0]
deviceOne_file = thermOneFolder + '/w1_slave'


#getting the temp from the output
def read_thermOnetemp():
    f=open(deviceOne_file, 'r')
    thermOnelines = f.readlines()
    f.close()
    #once in a while it throws an error. this gets a new temp if error is thrown
    while thermOnelines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        thermOnelines = read_thermOnetemp_raw()
    equals_pos = thermOnelines[1].find('t=')
    #if output looks fine, do this:
    if equals_pos != -1:
        temp_string = thermOnelines[1][equals_pos+2:]
        thermOnetemp_c = round(1.8*(float(temp_string) / 1000.0) +32, 2)
        return thermOnetemp_c

def timeAlarms(oldStatus):

    status = GPIO.input(airIntakeStatusPin)
    #reading in the raw output

    
    if abs(status-oldStatus) == 1:
        startingTemp = read_thermOnetemp()
        time.sleep(data["fireMonitorAlarmTimeInSeconds"])
        currentTemp = read_thermOnetemp()

        if (currentTemp - startingTemp) < data["minDegreesChangeToNotRaiseAlarm"]:
            timeEnd = time.time() + data["alarmRunTimeInSeconds"]
            while time.time() < timeEnd
                GPIO.output(data['alarmPin'], 1)
        
        else:
            print "Furnace is heating as expected."
            timeAlarms(status)

    else:
        timeAlarms(status)

        
timeAlarms(GPIO.input(airIntakeStatusPin))
        

    

GPIO.cleanup()
