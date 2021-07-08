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
            light.set_version(float(item["ver"])) # TODO: check if this needs to be converted to float
            light.set_socketPersistent(True)
    if not light:
        raise Exception(f"'{name}' light not found.")
    return light


# this kind of button toggles 1 light on short-press, and dims on long-press
class LightButton(ButtonDevice):
    def __init__(self, id, name, long_time=4):
        ButtonDevice.__init__(self, id, long_time)
        self.light = get_light(name)       

    def short_press(self):
        dt = datetime.now().strftime('%r %d/%m/%Y')
        print(f"{dt}: SHORT")
        data = self.light.status()
        if(data['dps']['20'] == True):
            self.light.turn_off()
        else:
            self.light.turn_on()
    
    # TODO: workout long action

    def long_press(self):
        dt = datetime.now().strftime('%r %d/%m/%Y')
        print(f"{dt}: LONG")
    
    def long_rolling(self):
        dt = datetime.now().strftime('%r %d/%m/%Y')
        print(f"{dt}: ROLLING")

# this kind of button turns all lights off on a short-press
class AllOffButton(ButtonDevice):
    def __init__(self, id, lights):
        ButtonDevice.__init__(self, id)
        self.lights = {}
        for name in lights:
            self.lights[name] = get_light(name)
    
    def short_press(self):
        dt = datetime.now().strftime('%r %d/%m/%Y')
        for name in self.lights:
            print(f"{dt}: {name} - Off")
            self.lights[name].turn_off()
    
    def long_press(self):
        pass
    
    def long_rolling(self):
        pass


# this is all the buttons we want to listen to
rooms = [
    LightButton(818562),                                         # hallway
    # LightButton(3764961, "Light_1"),                           # bigg
    # LightButton(835186, "Light_2"),                            # entrance
    # LightButton(3764962, "Leo's Light"),                       # leo_room
    # LightButton(3764964, "Light_3"),                           # my_room
    
    # AllOffButton(3764968, ["Light_1", "Light_2", "Light_3"]),  # all_off
]

# this is the main loop that calls process on all the buttons
while True:
    for room in rooms:
        room.process(rfdevice)
    time.sleep(0.01)
