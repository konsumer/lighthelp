#!/usr/bin/env python3

import time
from rpi_rf import RFDevice
from datetime import datetime
from button_device import ButtonDevice
import signal
import sys
import tinytuya
import json

with open('snapshot.json') as json_file:
    jdata = json.load(json_file)

rfdevice = RFDevice(gpio=27)
rfdevice.enable_rx()

# cleanup on exit


def signal_handler(sig, frame):
    rfdevice.cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# get a light by name


def get_light(name):
    light = None
    for item in jdata["devices"]:
        if item["name"] == name:
            light = tinytuya.BulbDevice(item["id"], item["ip"], item["key"])
            # TODO: check if this needs to be converted to float
            light.set_version(float(item["ver"]))
            light.set_socketPersistent(True)
        if not light:
            raise Exception(f"'{name}' light not found.")
    return light

# maps a single switch to multiple tinytuya light devices


class MultipleLightButton(ButtonDevice):
    def __init__(self, id, *lights):
        debounce = 1000
        long_time = 5000
        ButtonDevice.__init__(self, id, debounce, long_time)
        self.lights = {}
        self.statuses = {}
        self.pressing = False
        self.fade_up = True

        for name in lights:
            try:
                self.lights[name] = get_light(name)
            except:
                print(f"Light not found: {name}")

    def update_status(self):
        self.statuses = {}
        for name in self.lights:
            try:
                self.statuses[name] = self.lights[name].status()
            except:
                print(f"Failed to update status on {name}")

    def short_press(self):
        dt = datetime.now().strftime('%r %d/%m/%Y')
        # how to change print id number to words ie hallway
        print(f"{dt} ({self.id}): SHORT")
        self.update_status()
        for name in self.lights:
            # Edit for the other version of lights, I just added an 'or' on line 61
            # if you really need parallel on/off see https://stackoverflow.com/questions/7207309/how-to-run-functions-in-parallel

            if (self.statuses[name]['dps']['20'] == True):
                self.lights[name].turn_off()
            else:
                self.lights[name].turn_on()

    def long_rolling(self):
        """ called when button is pressed for a long time, in a rolling manner"""
        if not self.pressing:
            # one-time code goes here, runs at start of long press
            self.pressing = True
            self.update_status()

        # set new fade to relationship between current-fade and self.elapsed

        for name in self.lights:
            try:
                amountToFade = self.elapsed / 2000
                if self.fade_up:
                    newfade = self.lights[name].set_brightness_percentage(
                        +amountToFade)
                    newfade = self.lights[name].set_colourtemp_percentage(
                        +amountToFade)
                else:
                    newfade = self.lights[name].set_brightness_percentage(
                        -amountToFade)
                    newfade = self.lights[name].set_colourtemp_percentage(
                        -amountToFade)
                    if newfade > 100:
                        newfade = 100
                    if newfade < 0:
                        newfade = 0
                    self.statuses[name]['fade'] = newfade
                    self.lights[name].set_brightness_percentage(newfade)
            except:
                print(f"Could not fade {name}")

    def long_press(self):
        dt = datetime.now().strftime('%r %d/%m/%Y')
        print(f"{dt} ({self.id}): LONG")
        self.pressing = False
        self.fade_up = not self.fade_up


# this is all the buttons we want to listen to
rooms = [
    #    MultipleLightButton(3764961, "Leo's Light"),
    MultipleLightButton(835186, "Light_1", "Light_2", "Light_3"),  # entrance
    MultipleLightButton(818562, "Light_1", "Light_2", "Light_3")  # hallway
]

# this is the main loop that calls process on all the buttons
while True:
    for room in rooms:
        room.process(rfdevice)
    time.sleep(0.01)
