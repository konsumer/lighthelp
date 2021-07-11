#!/usr/bin/env python3

import time
from rpi_rf import RFDevice
from datetime import datetime
from button_device import ButtonDevice
import signal
import sys
from tinytuya import BulbDevice
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
    for item in jdata["devices"]:
        if item["name"] == name:
            light = BulbDevice(item["id"], item["ip"], item["key"])
            light.set_version(float(item["ver"]))
            light.set_socketPersistent(True)
            return light

# get a more friendly version of status


def get_friendly_status(light):
    status = light.status()
    out = {}
    try:
        out["power"] = status["dps"]["20"]
    except:
        out["power"] = status["dps"]["1"]

    # 10-1000
    try:
        fade = status["dps"]["22"]
    except:
        fade = status["dps"]["3"]

    # percent 0-100
    out["fade"] = (fade - 10) / 990

    return out


# maps a single switch to multiple tinytuya light devices
class MultipleLightButton(ButtonDevice):
    def __init__(self, id, *lights):
        debounce = 1000
        long_time = 5000
        ButtonDevice.__init__(self, id, debounce, long_time)
        self.button_name = buttons[id]
        self.lights = {}
        self.statuses = {}
        self.pressing = False
        self.fade_up = True

        for name in lights:
            try:
                self.lights[name] = get_light(name)
            except Exception as err:
                print(err)
                print(f"Light not found: {name}")

    def update_status(self):
        self.statuses = {}
        for name in self.lights:
            try:
                self.statuses[name] = get_friendly_status(self.lights[name])
            except:
                print(f"Failed to update status on {name}")

    def short_press(self):
        dt = datetime.now().strftime('%r %d/%m/%Y')
        # how to change print id number to words ie hallway
        print(f"{dt} ({self.button_name}): SHORT")
        self.update_status()
        for name in self.lights:
            try:
                if (self.statuses[name]['power'] == True):
                    self.lights[name].turn_off()
                else:
                    self.lights[name].turn_on()
            except:
                print(f"Could not toggle {name}")

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
                newFade = self.statuses[name]['fade']
                if self.fade_up:
                    newFade = newFade + amountToFade
                else:
                    newFade = newFade - amountToFade

                if newFade > 100:
                    newFade = 100
                if newFade < 0:
                    newFade = 0

                self.statuses[name]['fade'] = newFade
                self.lights[name].set_brightness_percentage(newFade)
            except:
                print(f"Could not fade {name}")

    def long_press(self):
        dt = datetime.now().strftime('%r %d/%m/%Y')
        print(f"{dt} ({self.button_name}): LONG")
        self.pressing = False
        self.fade_up = not self.fade_up

#list of button name
buttons = {
    3764961: "Leo's Buttons", 
    835186: "Entrance", 
    818562: "Hallway"
}

# this is all the buttons we want to listen to
rooms = [
    MultipleLightButton(3764961, "Leo's Light"),
    MultipleLightButton(835186, "Light_1", "Light_2", "Light_3"),  # entrance
    MultipleLightButton(818562, "Light_1", "Light_2", "Light_3")  # hallway
]

# this is the main loop that calls process on all the buttons
while True:
    for room in rooms:
        room.process(rfdevice)
    time.sleep(0.01)
