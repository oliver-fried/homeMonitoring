import os
import glob
import time

from guizero import App, Text




app.display()
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

while True:
    read_temp()
    if read_temp()> maxTemp:
        print("above 23")
    else:
        print(read_temp())
    time.sleep(1)

app = App(title="Hello world")
welcome_message = Text(app, text=read_temp(), size=40)

app.display()