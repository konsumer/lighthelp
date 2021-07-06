#!/usr/bin/env python3
            
"""
if press is longer than short_time but less than long_time, fire short
if press is longer than long_time, fire long
"""         
            

class ButtonDevice:
    def __init__(self, id, short_time=500, long_time=10000):
        self.id = id
        self.timestamp = 0
        self.short_time = short_time
        self.long_time = long_time
        self.last_button_time = 0
    
    def process(self, rfdevice):
        """ This processes current rfdevice and fires on_short or on_long"""
        if rfdevice.rx_code == self.id and rfdevice.rx_code_timestamp != None and rfdevice.rx_code_timestamp != self.timestamp:
            self.timestamp = rfdevice.rx_code_timestamp
            time_elapsed = self.timestamp - self.last_button_time
            self.last_button_time = self.timestamp
            if time_elapsed > self.short_time:
                # either a short or a long
                if time_elapsed > self.long_time:
                    self.on_long()
                else:
                    self.on_short()


    
