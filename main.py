from adafruit_macropad import MacroPad
from time import sleep
from macropadmanager import MacroPadManager
from gc import mem_free, collect


REFRESH_INTERVAL = 0.04

# Create macropad instance for interfacing.
macropad = MacroPad()

manager = MacroPadManager(
    macropad,
    './config.json'
)

while True:

    manager.update(REFRESH_INTERVAL)
    # collect()
    # print(mem_free())
        
    sleep(REFRESH_INTERVAL)

