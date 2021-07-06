#!/usr/bin/env python3

import time
from rpi_rf import RFDevice
from button_device import ButtonDevice

rfdevice = RFDevice(gpio=27)
rfdevice.enable_rx()

# Use a extension class to setup the callbacks.
# this is a generic one that will just print

class GenericButton(ButtonDevice):
    def on_short(self):
        print(f"short {self.id}!")
    
    def on_long(self):
        print(f"long {self.id}!")

# this is all the buttons we want to listen to
rooms = [
    GenericButton(818562),
    # GenericButton(835186),
    # GenericButton(835186),
    # GenericButton(3764962),
    # GenericButton(3764964)
]

# this is the main loop that calls process on all the buttons
while True:
    for room in rooms:
        room.process(rfdevice)
    time.sleep(0.01)

# cleanup device
rfdevice.cleanup()