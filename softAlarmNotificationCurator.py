#!/usr/bin/env python

try:
    f=open("softAlarmNotificationTracker.txt", "r")
    data = f.read()
    f.close()
except:
    print "ERROR: can't access softAlarmNotificationTracker text file!"

data.split("/")
mostRecentFour = data[-4:]


if len(data)>4:
    f=open("softAlarmNotificationTracker.txt", "w")
    f.write(mostRecentFour)
    f.close()
    
if len(data) == 0:
    mostRecentFour = "No recent alarms"
    
print mostRecentFour