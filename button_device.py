#!/usr/bin/env python3
         
import time
from datetime import date

class ButtonDevice:
    def __init__(self, id, debounce=2):
        self.id = id
        self.debounce = debounce
        self.oldtime = int(time.time()) - debounce
        self.inpress = False
    
    def process(self, rfdevice):
        """ This processes current rfdevice and fires on_short or on_long"""
        now = int(time.time())
        dt = date.today().strftime('%r %d/%m/%Y')
        if rfdevice.rx_code == self.id:
            if now - self.oldtime < self.debounce:
                # print("Ignoring Button Press Duplication")
                pass
            elif self.inpress:
                self.oldtime = now
                self.inpress = False
                self.power_on()
                print(f"{dt}: On")
            else:
                self.oldtime = now
                self.inpress = True
                self.power_off()
                print(f"{dt}: Off")
