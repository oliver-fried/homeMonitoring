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
maxTemp = ((data["maxTempF"]- 32)*(0.55555555555555))
maxSlope = data["maxSlopeC"]
thermSerialNumber = data["furnaceThermometerSerialNumber"]

#getting the therm file
thermOneFolder = glob.glob(base_dir + thermSerialNumber)[0]
deviceOne_file = thermOneFolder + '/w1_slave'

#setting up email sending
sender_email ='greenridgehomemonitoring@gmail.com'
rec_email = data['receivingEmail']
password = '1426Greenridge'
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, password)


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

statusArray = []

def timeAlarms(oldStatus):
    GPIO.output(data['alarmPin'], 0)

    status = GPIO.input(airIntakeStatusPin)
    #reading in the raw output

    if status-oldStatus == 1:
        startingTemp = read_thermOnetemp()
        time.sleep(data["fireMonitorAlarmTimeInSeconds"])
        currentTemp = read_thermOnetemp()

        if currentTemp >= startingTemp:
            print "Furnace is not cooling down!"
            server.sendmail(sender_email, rec_email, "WARNING! PLENUM IS NOT COOLING DOWN!")

            timeEnd = time.time() + data["alarmRunTimeInSeconds"]
            print "----------------------------------------------"
            print "the  temp recorded on the last iteration was: " + str(startingTemp)
            print "the temp recorded on this iteration is: " + str(currentTemp)
            print "air intake status: " + str(status)
            while time.time() < timeEnd:
                GPIO.output(data['alarmPin'], 1)

            GPIO.output(data['alarmPin'], 0)
            statusArray.insert(0, status)
            if len(statusArray) > 2:
                del statusArray[-1]
        
        else:
            print "----------------------------------------------"
            print "the  temp recorded on the last iteration was: " + str(startingTemp)
            print "the temp recorded on this iteration is: " + str(currentTemp)
            print "air intake status: " + str(status)
            statusArray.insert(0, status)
            if len(statusArray) > 2:
                del statusArray[-1]


    elif status-oldStatus == -1:
        startingTemp = read_thermOnetemp()
        time.sleep(data["fireMonitorAlarmTimeInSeconds"])
        currentTemp = read_thermOnetemp()

        if currentTemp <= startingTemp:
            print "Furnace is not warming up!"
            server.sendmail(sender_email, rec_email, "Attention! Plenum is not warming up. Fire has most likely died.")

            timeEnd = time.time() + data["alarmRunTimeInSeconds"]
            print "----------------------------------------------"
            print "the  temp recorded on the last iteration was: " + str(startingTemp)
            print "the temp recorded on this iteration is: " + str(currentTemp)
            print "air intake status: " + str(status)
            while time.time() < timeEnd:
                GPIO.output(data['alarmPin'], 1)
            GPIO.output(data["alarmPin"], 0)
            statusArray.insert(0, status)
            if len(statusArray) > 2:
                del statusArray[-1]
            
        else:
            print "----------------------------------------------"
            print "the  temp recorded on the last iteration was: " + str(startingTemp)
            print "the temp recorded on this iteration is: " + str(currentTemp)
            print "air intake status: " + str(status)
            statusArray.insert(0, status)
            if len(statusArray) > 2:
                del statusArray[-1]


    else:
        startingTemp = read_thermOnetemp()
        time.sleep(data["fireMonitorAlarmTimeInSeconds"])
        currentTemp = read_thermOnetemp()
        print "No change"
        print "----------------------------------------------"
        print "the  temp recorded on the last iteration was: " + str(startingTemp)
        print "the temp recorded on this iteration is: " + str(currentTemp)
        print "air intake status: " + str(status)
        statusArray.insert(0, status)
        if len(statusArray) > 2:
            del statusArray[-1]
        



statusArray.insert(0, GPIO.input(airIntakeStatusPin))

while True:
    timeAlarms(statusArray[0])


GPIO.cleanup()
