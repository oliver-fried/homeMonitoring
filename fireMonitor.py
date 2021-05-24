import os
import glob
import time
import RPi.GPIO as GPIO
import json
import smtplib

#  | OLIVER FRIED JAN 2021 | OLIVERFRIED3@GMAIL.COM |

#getting data from JSON file
with open('monitoringParameters.json') as f:
        #define the data inside the JSON file as "data." This will allow me to access it later on when I define variables.
        data = json.load(f)

#assigning value to varibles
airIntakeStatusPin = data['airIntakeStatusPin']
softAlarmPin = data["softAlarmPin"]
alarmRunTimeInSeconds = data["alarmRunTimeInSeconds"]
alarmOffTimeInSeconds = data["alarmOffTimeInSeconds"]
secondsBeforeUpdatingRate = data["secondsBeforeUpdatingRate"]

#setting up GPIO outputs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(airIntakeStatusPin, GPIO.IN)
GPIO.setup(softAlarmPin, GPIO.OUT)

#initialize the device
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#setup therm location
base_dir = '/sys/bus/w1/devices/'

#defining variables from JSON file
maxTemp = ((data["maxTempF"]- 32)*(0.55555555555555))
thermSerialNumber = data["furnaceThermometerSerialNumber"]

#getting the therm file
thermOneFolder = glob.glob(base_dir + thermSerialNumber)[0]
deviceOne_file = thermOneFolder + '/w1_slave'

#setting up email sending
sender_email ='greenridgehomemonitoring@gmail.com'
rec_email = data['receivingEmail']
password = '1426Greenridge'
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
except:
    print("ERROR: network is down, email not authenticated")

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

#this array keeps track of past 20 air intake status and the corresponding plenum temp
statusArray = []

def timeAlarms():
    #I set the alarm pin to low to make sure that there are no high outputs or anything
    GPIO.output(softAlarmPin, 0)

    #getting the current read of the air intake and temp, and their previous reads too.
    status = GPIO.input(airIntakeStatusPin)
    oldStatus = statusArray[0][0]
    temp = read_thermOnetemp()

    #This is a series of logic to see if there is a change in the air intake and whether we should sound the alarm or not
    if abs(status-oldStatus == 1):
        #this determines if there is a change in the air intake status so that we can pay attention to it later on
        statusArray.insert(0, (status, temp, 1))
    
    #this checks if there has been only one status change in the past 20 iterations, and if so, if its the last one in the array (longest ago)
    elif (sum(x.count(1) for x in statusArray) == 1) and (statusArray[-1][2] == 1):
        
        #getting the temp and status from that 20th iteration
        originalTemp = statusArray[-1][1]
        originalStatus = statusArray[-1][0]

        #this checks if the air intake status has closed since the last status change 
        if status-originalStatus == -1:
            #checking to see if the temp has not decreased since closing the air 
            if temp >= originalTemp:
                print("Furnace is not cooling down!")

                #I use this try except code here to try to send an email, but if not internet, then just skip over it with not issues
                try:
                    server.sendmail(sender_email, rec_email, "WARNING! PLENUM IS NOT COOLING DOWN!")
                except:
                    print("ERROR: network is down, email not working")

                #printing info to the console
                print "----------------------------------------------"
                print "the temp recorded on this iteration is: " + str(temp)
                print "the temp recorded at last status change " + str(originalTemp)
                print "air intake status: " + str(status)
                print "air intake status at last status change " + str(originalStatus)
                
                #sounding the alarm, similar procedure of that in policeSiren.py
                for x in range(5):

                    timeEnd = time.time() + alarmRunTimeInSeconds

                    while time.time() < timeEnd:
                        GPIO.output(softAlarmPin, 1)

                    timeOff = time.time() + alarmOffTimeInSeconds

                    while time.time() < timeOff:
                        GPIO.output(softAlarmPin, 0)

                #putting data into the array for the next iteration
                statusArray.insert(0, (status, temp, 0))

                #this keeps the length of the array fixed at 20 entries
                if len(statusArray) > 20:
                    del statusArray[-1]
            
            #if the temp is decreasing, this is what we print
            else:
                print "----------------------------------------------"
                print "COOLING AS NORMAL"
                print "the temp recorded on this iteration is: " + str(temp)
                print "the temp recorded at last status change " + str(originalTemp)
                print "air intake status: " + str(status)
                print "air intake status at last status change " + str(originalStatus)

                #putting data into the array for the next iteration
                statusArray.insert(0, (status, temp, 0))

                #keeping the length of the array fixed at 20
                if len(statusArray) > 20:
                    del statusArray[-1]


        #this checks if the air intake has opened since last status change 
        elif status-oldStatus == 1:
            

            if currentTemp <= startingTemp:
                print "Furnace is not warming up!"

                try:
                    server.sendmail(sender_email, rec_email, "Attention! Plenum is not warming up. Fire has most likely died.")
                except:
                    print "ERROR: network is down, email not working"
                        
                print "----------------------------------------------"
                print "the temp recorded on this iteration is: " + str(temp)
                print "the temp recorded at last status change " + str(originalTemp)
                print "air intake status: " + str(status)
                print "air intake status at last status change " + str(originalStatus)

                #sounding the alarm, similar procedure of that in policeSiren.py
                for x in range(5):

                    timeEnd = time.time() + alarmRunTimeInSeconds

                    while time.time() < timeEnd:
                        GPIO.output(softAlarmPin, 1)

                    timeOff = time.time() + alarmOffTimeInSeconds

                    while time.time() < timeOff:
                        GPIO.output(softAlarmPin, 0)


                #putting data into the array for the next iteration
                statusArray.insert(0, (status, temp, 0))

                #this keeps the length of the array fixed at 20 entries
                if len(statusArray) > 20:
                    del statusArray[-1]
                
            #If temp goes up, we print this
            else:
                print "----------------------------------------------"
                print "WARMING AS EXPECTED"
                print "the temp recorded on this iteration is: " + str(temp)
                print "the temp recorded at last status change " + str(originalTemp)
                print "air intake status: " + str(status)
                print "air intake status at last status change " + str(originalStatus)

                statusArray.insert(0, (status, temp, 0))
                if len(statusArray) > 20:
                    del statusArray[-1]

    #this is what we print if the iteration doesnt apply to any of the other statements above
    else:
        print "----------------------------------------------"
        print "No change"
        print "the  temp recorded on the last iteration was: " + str(statusArray[0][1])
        print "the temp recorded on this iteration is: " + str(temp)
        print "air intake status: " + str(status)
        print "the status from last iteration was " + str(statusArray[0][0])
        statusArray.insert(0, (status, temp, 0))
        if len(statusArray) > 20:
            del statusArray[-1]
        



statusArray.insert(0, (GPIO.input(airIntakeStatusPin), read_thermOnetemp(), 0))

while True:
    timeAlarms()
    time.sleep(secondsBeforeUpdatingRate)

GPIO.cleanup()
