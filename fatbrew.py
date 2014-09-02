import RPi.GPIO as GPIO

boardRevision = GPIO.RPI_REVISION
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#This will test the system
while True:
    if GPIO.input(22):
        flowpin = True
    else:
        flowpin = False
    print flowpin

