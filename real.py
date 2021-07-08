#!/usr/bin/env python3

import time
from rpi_rf import RFDevice
from button_device import DemoButton
import signal
import sys

rfdevice = RFDevice(gpio=27)
rfdevice.enable_rx()

# cleanup on exit
def signal_handler(sig, frame):
    rfdevice.cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# this is all the buttons we want to listen to
rooms = [
    DemoButton(818562),
    # DemoButton(835186),
    # DemoButton(835186),
    # DemoButton(3764962),
    # DemoButton(3764964)
]

# this is the main loop that calls process on all the buttons
while True:
    for room in rooms:
        room.process(rfdevice)
    time.sleep(0.01)
