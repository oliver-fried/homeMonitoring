import os
import glob
import time
from guizero import App, Text

app = App(title="Temperature Monitor", layout='grid')


#initialize the device
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
print(base_dir)

maxTemp = 23



device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f=open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def updateTempText():
    text.set(read_temp())
    text.after(1000, updateTempText)
    

if __name__ =='__main__':
    timeTitle = Text(app, time.ctime(), grid=[0,0], size=20)
    title = Text(app, "Furnace Temperature", grid=[0,1], size=20)
    text = Text(app, "Loading...", grid=[0,2], size=20)
    text.after(1000, updateTempText)

    app.display()


