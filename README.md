# light help

A friend is working on some cheap wireless switches & lights. This repo contains experiments & stuff to get them working.

- `real.py` - will eventually actually listen to the lightswitches
- `emulator.py` - a pygame emulator. Press space to act like the button.

Make sure you have pygame installed for emulator:

```
sudo apt install python3-pygame
```

Module button_device
====================

Classes
-------

## `ButtonDevice(id, debounce=1, long_time=4)`
>   Handle a radio-button - extend this to create your `short_press()` and `long_press()` methods.
    
* `id` - The id of the button
* `debounce` - The time (in ms) to wait before triggering short/long
* `long_time` - The time (in ms) to consider a "long press"

### Methods

`process(self, rfdevice)`
:   Process the current rfdevice. You should call this in a  loop.

#### callbacks

Implement these in your sub-class:

`long_press(self)`
:   called when button is pressed for a long time

`long_rolling(self)`
:    called when button is pressed for a long time, in a rolling manner

`short_press(self)`
:   called when button is pressed for a short time
