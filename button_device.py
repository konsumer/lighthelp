#!/usr/bin/env python3
         
import time
from datetime import datetime

# base-class for all button-actions
class ButtonDevice:
    """Handle a radio-button - extend this to create your `short_press()` and `long_press()` methods.

* `id` - The id of the button
* `debounce` - The time (in ms) to wait before triggering short/long
* `long_time` - The time (in ms) to consider a "long press"

"""
    def __init__(self, id, debounce = 250, long_time = 2000):
        self.id = id
        self.debounce = debounce
        self.long_time = long_time
        self.oldtime = int(time.time() * 1000) - debounce
        self.toggle = False
        self.oldtimestamp = 0
        self.pressed = False
        self.oldpressed = False
        self.onstart = 0
        self.elapsed = 0
    
    def process(self, rfdevice):
        """Process the current rfdevice. You should call this in a  loop."""
        now = int(time.time() * 1000)
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
            if self.elapsed < 100000:
                if self.elapsed > self.long_time:
                    self.long_press()
                else:
                    self.short_press() 
        self.oldpressed = self.pressed
 
        

# this is a button class that just prints the time
class DemoButton(ButtonDevice):
    """ Example class that extends `ButtonDevice` and just prints press-type and time"""
    def short_press(self):
        """ called when button is pressed for a short time"""
        dt = datetime.now().strftime('%r %d/%m/%Y')
        print(f"{dt}: SHORT")
    
    def long_press(self):
        """ called when button is pressed for a long time"""
        dt = datetime.now().strftime('%r %d/%m/%Y')
        print(f"{dt}: LONG")