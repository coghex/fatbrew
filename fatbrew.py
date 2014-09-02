import RPi.GPIO as GPIO
import os
import glob
import time

#The temperature sensor code comes from https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def readtempraw():
	catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out,err = catdata.communicate()
	out_decode = out.decode('utf-8')
	lines = out_decode.split('\n')
	return lines

def readtemp():
    lines = readtempraw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

boardRevision = GPIO.RPI_REVISION
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#This will test the system
while True:
    if GPIO.input(22):
        flowpin = True
    else:
        flowpin = False
    print "flow pin is " + flowpin
    print "temp is " + readtemp()

