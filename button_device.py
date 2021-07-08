#!/usr/bin/env python3
         
import time
from datetime import datetime

# base-class for all button-actions
class ButtonDevice:
    def __init__(self, id, debounce=2):
        self.id = id
        self.debounce = debounce
        self.oldtime = int(time.time()) - debounce
        self.inpress = False
    
    def process(self, rfdevice):
        """ This processes current rfdevice and fires on_short or on_long"""
        now = int(time.time())
        if rfdevice.rx_code == self.id:
            if now - self.oldtime < self.debounce:
                # print("Ignoring Button Press Duplication")
                pass
            elif self.inpress:
                self.oldtime = now
                self.inpress = False
                self.power_on()
            else:
                self.oldtime = now
                self.inpress = True
                self.power_off()

# this is a button class that just prints the time
class DemoButton(ButtonDevice):
    def power_on(self):
        dt = datetime.now().strftime('%r %d/%m/%Y')
        print(f"{dt}: On")
    
    def power_off(self):
        dt = datetime.now().strftime('%r %d/%m/%Y')
        print(f"{dt}: Off")