from adafruit_macropad import MacroPad
from time import sleep
from macropadmanager import MacroPadManager


REFRESH_INTERVAL = 0.04

# Create macropad instance for interfacing.
macropad = MacroPad()

manager = MacroPadManager(
    macropad,
    './config.json'
)

while True:

    manager.update(REFRESH_INTERVAL)
        
    sleep(REFRESH_INTERVAL)

