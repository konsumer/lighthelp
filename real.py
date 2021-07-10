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

# maps a single switch to multiple tinytuya light devices
class MultipleLightButton(ButtonDevice):
    def __init__(self, id, *lights):
        debounce = 250
        long_time = 2000
        ButtonDevice.__init__(self, id, debounce, long_time)
        self.lights = {}
        for name in lights:
            self.lights[name] = get_light(name)
    
    def short_press(self):
        dt = datetime.now().strftime('%r %d/%m/%Y')
        print(f"{dt}: SHORT")
        for name in self.lights:
            data = self.lights[name].status()
            if (data['dps']['20'] == True):
                self.lights[name].turn_off()
            else:
                self.lights[name].turn_on()
        
        

# this is all the buttons we want to listen to
rooms = [
#    MultipleLightButton(3764962, "Leo's Light"),
    MultipleLightButton(835186, "Light_1", "Light_2", "Light_3"), # entrance
    MultipleLightButton(818562, "Light_1", "Light_2", "Light_3")  # hallway
]

# this is the main loop that calls process on all the buttons
while True:
    for room in rooms:
        room.process(rfdevice)
    time.sleep(0.01)
