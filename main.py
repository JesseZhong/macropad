from adafruit_macropad import MacroPad
from time import sleep
from macropadmanager import MacroPadManager
from components.utils import file_exists
# from gc import mem_free, collect

BAKED_CONFIG = './config.baked.json'
REFRESH_INTERVAL = 0.04

# Create macropad instance for interfacing.
macropad = MacroPad()

manager = MacroPadManager(
    macropad,
    BAKED_CONFIG if file_exists(BAKED_CONFIG) else './config.json'
)

while True:

    manager.update(REFRESH_INTERVAL)
    # collect()
    # print(mem_free())
        
    sleep(REFRESH_INTERVAL)

