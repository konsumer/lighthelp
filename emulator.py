#!/usr/bin/env python3

"""
This will emulate the lightsiwtch setup 
"""

import pygame
import time
from button_device import ButtonDevice

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Use a extension class to setup the callbacks.
# this is a generic one that will just print

class GenericButton(ButtonDevice):
    def power_on(self):
        print("POWER ON CALLBACK")
    def power_off(self):
        print("POWER OFF CALLBACK")

switch = GenericButton(818562)

# this is the rect drawn on screen for the switch
rect = pygame.Rect(10, 10, 100, 100)

# this emulates the rfdevice
class FakeRFDevice:
    def __init__(self, code, pulselength, proto=1):
        self.rx_code_timestamp = int(time.perf_counter() * 1000000)
        self.rx_code = code
        self.rx_pulselength = pulselength
        self.rx_proto = proto


def main():
    print("Pretend spacebar is the button")
    while True:
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if pressed[pygame.K_SPACE]:
            color = pygame.Color(0, 255, 0)
            rfdevice = FakeRFDevice(818562, 320, 1)
            # this would normally be called in a loop with a delay
            switch.process(rfdevice)
        else:
            color = pygame.Color(255, 0, 0)
        
        pygame.draw.rect(screen, color, rect)

        pygame.display.flip()
        clock.tick(60)

main()