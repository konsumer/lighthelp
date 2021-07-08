#!/usr/bin/env python3

"""
This will emulate the lightsiwtch setup 
"""

# disable the hello
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import time
from button_device import ButtonDevice
from random import randint

pygame.init()
pygame.font.init()
pygame.display.set_caption('Switch Emulator')
screen = pygame.display.set_mode((320, 210))
font = pygame.font.Font(pygame.font.get_default_font(), 20)

switch = ButtonDevice(818562)

# this is the rect drawn on screen for the switch
rect = pygame.Rect(100, 50, 100, 100)

# this emulates the rfdevice
class FakeRFDevice:
    def __init__(self, code, pulselength, proto=1):
        self.rx_code_timestamp = int(time.perf_counter() * 1000000)
        self.rx_code = code
        self.rx_pulselength = pulselength
        self.rx_proto = proto

def main():
    rfdevice = FakeRFDevice(818562, 320, 1)

    # I use these to fire more process than messages
    i = 0

    while True:
        i += 1
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if pressed[pygame.K_SPACE]:
            color = pygame.Color(0, 255, 0)
            # only update rfdevice every 10 frames
            if i % 10 == 0:
                rfdevice = FakeRFDevice(818562, randint(100, 400), 1)
            # send some random device
            switch.process(FakeRFDevice(randint(500000, 999999), randint(100, 400), 1))
        else:
            color = pygame.Color(255, 0, 0)

        # this would normally be called in a loop with a delay
        switch.process(rfdevice)

        screen.fill((0,0,0))
        text1 = font.render("Pretend spacebar is the button", True, (255, 255, 255))
        screen.blit(text1, (10, 10))
        text2 = font.render(f"Elapsed time: {switch.elapsed}", True, color)
        screen.blit(text2, (80, 180))
        pygame.draw.rect(screen, color, rect)

        pygame.display.flip()

main()