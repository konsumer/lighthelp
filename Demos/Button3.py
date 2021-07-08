#!/usr/bin/env python3
import signal
import sys
import time
#import my_room
from rpi_rf import RFDevice
from button import *
rfdevice = None


P_BUTTON = RFDevice(gpio=27)
#P_LED = 7     # adapt to your wiring

def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, exithandler)

rfdevice = RFDevice(gpio=27)
rfdevice.enable_rx()
timestamp = None

def setup():
    #GPIO.setmode(GPIO.BOARD)
    #GPIO.setup(P_LED, GPIO.OUT)
    
    button = Button(P_BUTTON) 
    button.addXButtonListener(onButtonEvent)

def onButtonEvent(button, event):
    global isRunning
    if event == BUTTON_PRESSED:
        print ("pressed")
    elif event == BUTTON_RELEASED:
        print ("released")
    elif event == BUTTON_LONGPRESSED:
       print ("long pressed")
    elif event == BUTTON_CLICKED:
        print ("clicked")
    elif event == BUTTON_DOUBLECLICKED:
        print ("double clicked")
        isRunning = False
       
setup()
isRunning = True
while isRunning:
    GPIO.output(P_LED, GPIO.HIGH)    
    time.sleep(0.1)
    GPIO.output(P_LED, GPIO.LOW)    
    time.sleep(0.1)
GPIO.cleanup()
print ("all done")
