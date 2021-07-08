# light help

A friend is working on some cheap wireless switches & lights. This repo contains experiments & stuff to get them working.

- `real.py` is what will eventually actually listen to the lightswitches
- `emulator.py` is a pygame emulator. Press space to act like the button

Make sure you have pygame installed for emulator:

```
sudo apt install python3-pygame
```

Module button_device
====================

Classes
-------

## `ButtonDevice(id, debounce=1, long_time=4)`
:   Handle a radio-button - extend this to create your `short_press()` and `long_press()` methods.
    
* `id` - The id of the button
* `debounce` - The time (in seconds) to wait before triggering short/long
* `long_time` - The time (in seconds) to consider a "long press"

### Methods

`process(self, rfdevice)`
:   Process the current rfdevice. You should call this in a  loop.
    * `id` - The id of the button
    * `debounce` - The time (in seconds) to wait before triggering short/long
    * `long_time` - The time (in seconds) to consider a "long press"

## `DemoButton(id, debounce=1, long_time=4)`
:   Example class that extends `ButtonDevice` and just prints press-type and time


### Methods

`long_press(self)`
:   called when button is pressed for a long time

`short_press(self)`
:   called when button is pressed for a short time
