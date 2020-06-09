# Code by @deividfoggi
# This code is for Raspberry Pi tested on Pi 4
# It is considering the usage of externals DS18B20 temp sensor connected as parasite
# This code will look for all temperature sensors under /sys/bus/w1/device starting with string 28
# Instructions to setup hardware and OS to detect the sensors at 

# Import modules
import os
import glob
import time
 
# Run shell commands to load modules in kernel
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
# Define base dir variable
base_dir = '/sys/bus/w1/devices/'
# Create an array including all directories listed in base dir starting with string 28
device_folder = glob.glob(base_dir + '28*')

# Function to read temperature in raw format
def read_temp_raw(device):
    # Append file name string which contains the current sensor read
    device = device + '/w1_slave'
    # Open the file in read mode
    f = open(device, 'r')
    # Create an array containing all lines (2 lines usually)
    lines = f.readlines()
    # Close the file
    f.close()
    # Return the lines
    return lines

# Function to format temperature in human readable format in Celsius
def read_temp(device_folder_string):
    # Create an array containing lines returned by function
    lines = read_temp_raw(device_folder_string)
    # While lines have no YES for CRC status
    while lines[0].strip()[-3:] != 'YES':
        # Wait for 200ms and try to read file again
        time.sleep(0.2)
        lines = read_temp_raw(device_folder_string)
    # Varaible containting the line with the temperature value (second line with 't=' string)
    equals_pos = lines[1].find('t=')
    # If the variable is not -1
    if equals_pos != -1:
        # Get the value in line 2 after 't='
        temp_string = lines[1][equals_pos+2:]
        # Convert the value to float (default sensor resolution is 5 caracters / 12-bit. For examploe 22550 is the raw value for 22.55 Celsius, it will change if sensor resolution is reconfigured to use more or less bytes)
        temp_c = float(temp_string) / 1000.0
        # Return the temperature read in float format
        return temp_c

# Forever while to build an array of objects containing the temperature read of each sensor temperature and print them in one line.
# Maybe not really good if you have 3 or more sensors
while True:
    # Create an empty array to store all sensors read
    sensors = []
    # For each sensor found in base folder (directories starting with string 28)
    for x in device_folder:
        # Append to the array the sensor read in float format
        sensors.append(x + ': ' + str(read_temp(x)))
    print(sensors)
    # Wait 750ms to read again. It is the recomended value considering the default sensor resolution at power-up which is 12-bit, resulting in up to 750ms converstion time: https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf
    time.sleep(0.750)
