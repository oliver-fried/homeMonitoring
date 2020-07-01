# homeMonitoring
Hi Grandpa, here are the instructions to get the home monitoring website running.
Unfortunately, I was not able to get tons done. 
Here are the things you need to do to get this working.

THIS SHOULD ALL BE DONE ON THE RP.

1. First you want to clone the repository. You'll want to go
to your existing folder with the home monitoring info and 
delete it completely. Then go to your command prompt and cd to where
you want to put the new homeMonitoring folder. Then, type
"git clone https://github.com/oliver-fried/homeMonitoring.git"
Then put in your username and password and there you go.

2. Now you will see many new files. Head over to 
"monitoringParameters.json". Open that up. Then, 
chance the serial numbers of "furnaceThermometerSerialNumber"
and "houseThermometerSerialNumber" to the furnace and house thermometer
serial numbers, respectively. If you don't know how to do this, refer
to the private eyepip tutorial.

    Essentially, you want to to type 'cd /sys/bus/w1/devices/' and then type 'ls' 
    You will see a listing of the current directory. There should be a directory 
    that is the serial number of your temperature gauge.
    This is taken directly from the private eye pi tutorial you had me do. If you 
    have questions about this part refer to the tutorial where it has you get the 
    thermometer serial number.
    
3. Now go back to the monitoringParameters.json file. I will list each parameter and 
explain what it does. Change these at will, but many of them are not functional :(

    "maxTempC": this is the maximum temp the furnace is allowed to reach.
    
    "maxSlopeC": this is the maximum rate the furnace temp can increase. If it increases too fast, we assume its an error.
    
    "furnaceThermometerSerialNumber": furnace thermometer serial number
    
    "houseThermometerSerialNumber": house thermometer serial number
    
    "alarmPin": this is the GPIO (NOT BCM) that the alarm is hooked into.
    
    "airIntakePin": this is the pin that one would use to control air intake, but it is CURRENTLY NOT FUNCTIONAL.
    
    "airIntakePinHighTimeInSeconds": this is how long one would have the airIntake pin in the high position to close the air intake (different motors take different amounts of time to close the intake.
    
    "airIntakeStatusPin": this is the pin that would read the air intake status.
    
    "receivingEmail": this is the email that alerts are sent to.

4. Now go to index.php. It should be in your homeMonitoring directory. Go to line 19 in index.php. Change "/home/pi/src/homeMonitoring/" to the location of your homeMonitoring files.

5. Now look at line 24. This is where i was trying to execute a shell command that would get me the status of pin 15. I was using "http://wiringpi.com/" to let me execute this command. I believe wiringpi is a library that lets the user type commands like "gpio read 15" right into the shell. It comes pre-installed on your RP. Try it on your RP and see what you think.
I'm really not sure if I can get the status of pins just by typing "gpio read 15" or whatever.
All I'm trying to do here is get the pin value corresponding to the air intake status. I'm not sure if using wiringpi and typing "gpio read 15" into the terminal is the right way to do this. BY THE WAY, I believe that wiringpi uses its own pin numbering system, so if you want to use the command "gpio read 15", you are not reading the BOARD pin 15, but instead the wiringpi pin 15. It is all very complicated. 

6. In lines 21 and 32 of index.php, I am running a 2 python files to get the temp of the both the furnace and the house. I tried using a python script to get GPIO pin status, but it seemed to just simply not run on my index.php website. This was very frustrating. Maybe it would work for you. 

7. In line 117-119, I am essentially using a php command that checks an array to see if the button I created above has been pressed and thus added to the array. I THINK this is what is going on. In the end, when I click the control air intake button, the index.php page will reload as it calls the command I wrote in line 119. "gpio write 15 1" makes wiringPi pin 15 high. Again, I am not certain if this actually works. I'm sorry about this!

8. Now put the index.php file in the directory /vars/www/html on your RP. I belive that is the correct directory, but just put it where you put your websites. Delete the old index.php file. Make sure you are not deleting the wrong one!

9. Now go back to the houseMonitoring file, and open up 'plenumTemp.py'. Go to line 14 and change '/home/pi/src/homeMonitoring/monitoringParameters.json' to the location of 'monitorinParameters.json' on your machine. It should still be in the homeMonitoring folder, but that folder is probably somewhere different than mine.

10. Do the exact same for houseTemp.py. Go to line 15 and make the necessary changes to the path.

11. Now go to the furnace alarm folder. this should be in your homeMonitoring folder. Open up 'parameters.json' and change the parameters like you did for the other json file earlier. This means: make sure the serial number correspondes to your furnace serial number. Make sure the alarm pin is correct. Make sure the email is correct. Make sure the max temp and slope are correct. 

12. I want to be clear here. The 'alarmTrigger.py' file should work. This means that I would suggest that you attach a furnace thermometer and siren to your RP  and then go to your command prompt on your RP and cd to the furnaceAlarm folder, and then type 'python alarmTrigger.py'. This should start a program that will continuously check if your plenum is too hot and then set off an alarm if it is, as well as sending you an email. This seem like it could be very useful.

13. That is it for now. I have to go do some other work before I leave for The Academy in about 3 hours. I really hope this makes some sense, and I feel bad because I didnt get too much done. I want to get it to work for you, so when i have some free time this fall i want to see if i can work on it. Alright thats it for now. Oliver over and out. 
    
