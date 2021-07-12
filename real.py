#!/usr/bin/env python3

import time
from rpi_rf import RFDevice
from datetime import datetime
from button_device import ButtonDevice
import signal
import sys
from tinytuya import BulbDevice
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
	for item in jdata["devices"]:
		if item["name"] == name:
			light = BulbDevice(item["id"], item["ip"], item["key"])
			light.set_version(float(item["ver"]))
			light.set_socketPersistent(True)
			return light

# get a more friendly version of status
def get_friendly_status(light):
	status = light.status()
	out = {}
	try:
		out["power"] = status["dps"]["20"]
	except:
		out["power"] = status["dps"]["1"]

	# 10-1000
	try:
		fade = status["dps"]["22"]
	except:
		fade = status["dps"]["3"]

	# percent 0-100
	out["fade"] = ((fade - 10.0) / 990.0) * 100.0
	return out

# maps a single switch to multiple tinytuya light devices
class MultipleLightButton(ButtonDevice):
	def __init__(self, id, *lights, debug=True):
		self.debug = debug
		debounce = 1000.0
		long_time = 5000.0
		ButtonDevice.__init__(self, id, debounce, long_time)
		self.button_name = buttons[id]
		self.lights = {}
		self.statuses = {}
		self.pressing = False
		self.fade_up = True

		for name in lights:
			try:
				self.lights[name] = get_light(name)
			except:
				self.log('ERROR', f"Light not found: {name}")

	def log(self, action, message):
		if self.debug:
			dt = datetime.now().strftime('%r %d/%m/%Y')
			print(f"{dt}\t{self.button_name}\t{action}\t{message}")

	def fade_lights(self, amountToFade):
		for name in self.lights:
			newFade = self.statuses[name]['fade']
			newFade = newFade + amountToFade
			if newFade > 100.0:
				newFade = 100.0
			if newFade < 0.0:
				newFade = 0.0
			self.statuses[name]['fade'] = newFade
			self.lights[name].set_brightness_percentage(float(newFade))

	def update_status(self):
		self.statuses = {}
		for name in self.lights:
			try:
				self.statuses[name] = get_friendly_status(self.lights[name])
			except:
				self.log('ERROR', f"Failed to update status on {name}")

	def short_press(self):
		# how to change print id number to words ie hallway
		self.update_status()
		for name in self.lights:
			self.log(
				'SHORT', f"Toggle {name} to {not self.statuses[name]['power']}")
			try:
				if self.lights[name]:
					self.lights[name] = get_light(name)

				if (self.statuses[name]['power'] == True):
					self.lights[name].turn_off()
				else:
					self.lights[name].turn_on()
			except:
				self.log('ERROR', f"Could not toggle {name}")

	def long_rolling(self):
		""" called when button is pressed for a long time, in a rolling manner"""
		if not self.pressing:
			# one-time code goes here, runs at start of long press
			self.pressing = True
			self.update_status()

		# set new fade to relationship between current-fade and self.elapsed

		for name in self.lights:
			try:
				amountToFade = self.elapsed / 2000.0
				if not self.fade_up:
					amountToFade = amountToFade * -1.0
				self.fade_lights(amountToFade)
				self.log(
					'ROLLING', f"Fade {name} up from {self.statuses[name]['fade']} by {amountToFade}")
			except:
				self.log('ERROR', f"Could not fade {name}")

	def long_press(self):
		self.log('LONG', "Toggle pressing to False")
		self.pressing = False
		self.fade_up = not self.fade_up


class FadeUpButton(MultipleLightButton):
	def short_press(self):
		amountToFade = 10.0
		self.update_status()
		self.fade_lights(amountToFade)
		for name in self.lights:
			self.log('SHORT', f"Fade {name} up from {self.statuses[name]['fade']} by {amountToFade}")

	def long_press(self):
		self.log('LONG', "Make sure fade up is True")
		self.pressing = False
		self.fade_up = True


class FadeDownButton(MultipleLightButton):
	def short_press(self):
		amountToFade = -10.0
		self.update_status()
		self.fade_lights(amountToFade)
		for name in self.lights:
			self.log('SHORT', f"Fade {name} down from {self.statuses[name]['fade']} by {amountToFade}")

	def long_press(self):
		self.log('LONG', "Make sure fade up is False")
		self.pressing = False
		self.fade_up = False


# list of button name, look up by ID
buttons = {
	3764961: "Leo Toggle",
	835186: "Entrance",
	818562: "Hallway",
	3764962: "Leo FadeUp",
	3764964: "Leo FadeDown"
}

# reverse-dictionary for looking ID up by name
b = {}
for id in buttons:
	b[buttons[id]] = id

# this is all the buttons we want to listen to
rooms = [
	MultipleLightButton(b["Leo Toggle"], "Leo's Light"),
	FadeUpButton(b["Leo FadeUp"], "Leo's Light"),
	FadeDownButton(b["Leo FadeDown"], "Leo's Light"),

	MultipleLightButton(b["Entrance"], "Light_1", "Light_2", "Light_3"),
	MultipleLightButton(b["Hallway"], "Light_1", "Light_2", "Light_3")
]

# this is the main loop that calls process on all the buttons
while True:
	for room in rooms:
		room.process(rfdevice)
	time.sleep(0.01)
