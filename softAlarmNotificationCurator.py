#!/usr/bin/env python


f=open("/home/pi/TechnicalStuff/WorkingAlarmSystemCode/Code/softAlarmNotificationTracker.txt", "r")
data = f.read()
f.close()


data.split("/")
mostRecentFour = data[-4:]


if len(data)>4:
    f=open("softAlarmNotificationTracker.txt", "w")
    f.write(mostRecentFour)
    f.close()
    
if len(data) == 0:
    mostRecentFour = "No recent alarms"
    
print mostRecentFour