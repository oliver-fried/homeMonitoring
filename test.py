#Hey Grandpa!
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

thermOneFolder = glob.glob(base_dir + '28*')[0]
deviceOne_file = thermOneFolder + '/w1_slave'

thermTwoFolder = glob.glob(base_dir + '28*')[0]
deviceTwo_file = thermTwoFolder + '/w1_slave'

def read_thermOnetemp_raw():
    f=open(deviceOne_file, 'r')
    thermOnelines = f.readlines()
    f.close()
    return thermOnelines

def read_thermTwotemp_raw():
    f=open(deviceTwo_file, 'r')
    thermTwolines = f.readlines()
    f.close()
    return thermTwolines

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

def read_thermTwotemp():
    thermTwolines = read_thermTwotemp_raw()
    while thermTwolines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        thermtwolines = read_thermTwotemp_raw()
    equals_pos = thermTwolines[1].find('t=')
    if equals_pos != -1:
        temp_string = thermTwolines[1][equals_pos+2:]
        thermTwotemp_c = float(temp_string) / 1000.0
        return thermTwotemp_c


def updateText():
    thermOneTemp.set(read_thermOnetemp())
    thermTwoTemp.set(read_thermTwotemp())
    timeTitle.set(time.ctime())
    text.after(1000, updateText)

def systemStatus():
    return "Armed"


class ConnectPage(GridLayout):
    # runs on initialization
    def __init__(self, **kwargs):
        # we want to run __init__ of both ConnectPage AAAAND GridLayout
        super().__init__(**kwargs)

        self.cols = 2  # used for our grid

        # widgets added in order, so mind the order.
        self.add_widget(Label(text="Current Time:"))  # widget #1, top left
        self.add_widget(Label(text=time.ctime())) # widget #2, top right

        self.add_widget(Label(text="System Status"))
        self.add_widget(Label(text=systemStatus()))

class AppOne(App):
    def build(self):
        return Label(text="test")

if __name__ =='__main__':
    '''timeTitle = Text(app, "Loading...", grid=[0,0], size=20)
    thermOneTitle = Text(app, "Furnace Temperature", grid=[0,1], size=20)
    thermOneTemp = Text(app, "Loading...", grid=[0,2], size=20)
    thermTwoTitle = Text(app, "House Temperature", grid=[0,1], size=20)
    thermTwoTemp = Text(app, "Loading...", grid=[0,2], size=20)
    updateText()'''

    AppOne().run()

    





