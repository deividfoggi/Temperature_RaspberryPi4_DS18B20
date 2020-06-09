# Code by @deividfoggi
# This code is for Raspberry Pi tested on Pi 4
# It is considering the usage of externals DS18B20 temp sensor connected as parasite
# This code will look for all temperature sensors under /sys/bus/w1/device starting with string 28
# Instructions to setup hardware and OS to detect the sensors at 

import os
import glob
import time
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')

def read_temp_raw(device):
    device = device + '/w1_slave'
    f = open(device, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_folder_string):
    lines = read_temp_raw(device_folder_string)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_folder_string)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

while True:
    sensors = []
    for x in device_folder:
        sensors.append(x + ': ' + str(read_temp(x)))
        time.sleep(0.5)
    print(sensors)
