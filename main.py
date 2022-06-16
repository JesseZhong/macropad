from adafruit_macropad import MacroPad
from time import sleep
from macropadmanager import MacroPadManager


REFRESH_INTERVAL = 0.04

# Create macropad instance for interfacing.
macropad = MacroPad()

manager = MacroPadManager(macropad)

macropad.pixels.fill((0, 255, 128))

while True:

    manager.handle_inputs()
        
    sleep(REFRESH_INTERVAL)

