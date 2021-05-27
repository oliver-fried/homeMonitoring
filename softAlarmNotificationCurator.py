#!/usr/bin/env python

try:
    f=open("softAlarmNotificationTracker.txt", "r")
    data = f.read()
    f.close()
except:
    print "ERROR: can't access softAlarmNotificationTracker text file!"


splitData = data.split("/")
mostRecentFour = splitData[-4:]



if len(splitData)>4:
    lessData = mostRecentFour[0] + "/" + mostRecentFour[1] + "/" + mostRecentFour[2] + "/" + mostRecentFour[3] + "/"
    f=open("softAlarmNotificationTracker.txt", "w")
    f.write(lessData)
    f.close()

if data == None:
    mostRecentFour = "No recent alarms"
    print mostRecentFour

else:
    print mostRecentFour
    

