import RPi.GPIO as GPIO
import os
import glob
import time
from ds18b20 import DS18B20

#attach liquid flow meter to pin 22 and temperature sensor to pin 4
pouring1 = False
lastPinState1 = False
pinState1 = 0
lastPinChange1 = int(time.time() * 1000)
pourStart1 = 0
pinChange1 = lastPinChange1
pinDelta1 = 0
hertz1 = 0
flow1 = 0
litersPoured1 = 0
pintsPoured1 = 0
pouring2 = False
lastPinState2 = False
pinState2 = 0
lastPinChange2 = int(time.time() * 1000)
pourStart2 = 0
pinChange2 = lastPinChange2
pinDelta2 = 0
hertz2 = 0
flow2 = 0
litersPoured2 = 0
pintsPoured2 = 0
#the temperature sensor library is here: https://github.com/timofurrer/ds18b20
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
sensor = DS18B20()

boardRevision = GPIO.RPI_REVISION
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#This will test the system
while True:
    currentTime = int(time.time() * 1000)
    if GPIO.input(22):
      pinState1 = True
    else:
      pinState1 = False
    if(pinState1 != lastPinState1 and pinState1 == True):
      if(pouring1 == False):
        pourStart1 = currentTime
      pouring1 = True
      pinChange1 = currentTime
      pinDelta1 = pinChange1 - lastPinChange1
      if (pinDelta1 < 1000 and pinDelta1 is not 0):
        hertz1 = 1000.0000 / pinDelta1
        flow1 = hertz1 / (60 * 7.5) # L/s
        litersPoured1 += flow1 * (pinDelta1 / 1000.0000)
        pintsPoured1 = litersPoured1 * 2.11338
        print(str(pintsPoured1) + " pints poured out of tap 1")

    if GPIO.input(23):
      pinState2 = True
    else:
      pinState2 = False
    if(pinState2 != lastPinState2 and pinState2 == True):
      if(pouring2 == False):
        pourStart2 = currentTime
      pouring2 = True
      pinChange2 = currentTime
      pinDelta2 = pinChange2 - lastPinChange2
      if (pinDelta2 < 1000 and pinDelta2 is not 0):
        hertz2 = 1000.0000 / pinDelta2
        flow2 = hertz2 / (60 * 7.5) # L/s
        litersPoured2 += flow2 * (pinDelta2 / 1000.0000)
        pintsPoured2 = litersPoured2 * 2.11338
        print(str(pintsPoured2) + " pints poured out of tap 2")
    if not (currentTime % 100000):
      print("temp is " + str(sensor.get_temperature()))
    lastPinChange1 = pinChange1
    lastPinState1 = pinState1

