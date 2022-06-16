try:
    from typing import Dict
except ImportError:
    pass

from adafruit_macropad import MacroPad
from traceback import print_exception
from time import sleep
from json import load
from macro import Macro


REFRESH_INTERVAL = 0.04

# Create macropad instance for interfacing.
macropad = MacroPad()

# Import macros.
macros: Dict[str, Macro] = {}
with open(
    './config.json',
    'rt',
    encoding='UTF-8'
) as file:
    data: Dict = load(file)

    if data:
        for macro_key, macro_config in data.items():
            macros[macro_key] = Macro(
                macropad,
                macro_config
            )


def handle(macro_key: str):
    if macro_key in macros:
        macros[macro_key].send()


macropad.pixels.fill((0, 255, 128))

# Track the initial state of the rotary encoder.
rotary_previous = macropad.encoder

while True:

    # Dequeue all current key events.
    while True:
        event = macropad.keys.events.get()

        # Break out when there are no more events.
        if not event:
            break

        # Check for for a key code.
        code = event.key_number
        if code != None:
            
            if event.pressed:
                try:
                    handle(str(code))
                except Exception as e:
                    print_exception(e, e, e.__traceback__)

    # Track any change in the rotary encoder.
    rotary_current = macropad.encoder

    # Interpret positive/clockwise rotations as
    # volume up, negative/cc as volume down.
    if rotary_previous != rotary_current:

        if (rotary_previous - rotary_current) > 0:
            handle('-')
        else:
            handle('+')

    rotary_previous = rotary_current
        
    sleep(REFRESH_INTERVAL)

