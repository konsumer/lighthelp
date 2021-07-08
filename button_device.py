#!/usr/bin/env python3
         
import time
from datetime import datetime

# base-class for all button-actions
class ButtonDevice:
    def __init__(self, id, debounce=2):
        self.id = id
        self.debounce = debounce
        self.oldtime = int(time.time()) - debounce
        self.toggle = False
        self.oldtimestamp = 0
        self.pressed = False
        self.oldpressed = False
        self.onstart = 0
        self.elapsed = 0
    
    def process(self, rfdevice):
        now = int(time.time())
        if rfdevice.rx_code_timestamp != self.oldtimestamp:
            self.oldtimestamp = rfdevice.rx_code_timestamp
            if rfdevice.rx_code == self.id:
                self.pressed = True
                self.oldtime = now
        else:
            if now > (self.oldtime + self.debounce):
                self.oldtime = now
                self.pressed = False
        if not self.oldpressed and self.pressed:
            self.onstart = now
        if self.oldpressed and not self.pressed:
            self.elapsed = now - self.onstart
            if self.elapsed > 5:
                self.long_press()
            else:
               self.short_press() 
        self.oldpressed = self.pressed
 
        

# this is a button class that just prints the time
class DemoButton(ButtonDevice):
    def short_press(self):
        dt = datetime.now().strftime('%r %d/%m/%Y')
        print(f"{dt}: SHORT")
    
    def long_press(self):
        dt = datetime.now().strftime('%r %d/%m/%Y')
        print(f"{dt}: LONG")