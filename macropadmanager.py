try:
    from typing import Dict
except ImportError:
    pass

from adafruit_macropad import MacroPad
from traceback import print_exception
from json import load
from components.display import Display
from components.macro import Macros
from components.ledpixel import LEDPixel


class MacroPadManager:

    def __init__(
        self,
        macropad: MacroPad,
        config_file: str
    ):
        self.macropad = macropad

        # Import config.
        with open(
            config_file,
            'rt',
            encoding='UTF-8'
        ) as file:

            data: Dict = load(file)

            if data:

                # Load display settings.
                self.display = Display(
                    data['display'] if 'display' in data else None,
                    self.macropad
                )

                # Load macros.
                self.macros = Macros(
                    data['macros'] if 'macros' in data else None,
                    self.macropad,
                    self.display
                )

                # Load LED settings.
                self.leds = LEDPixel(
                    data['leds'] if 'leds' in data else None,
                    self.macropad
                )

        # Track the initial state of the rotary encoder.
        self.rotary_previous = self.macropad.encoder


    def handle_inputs(self):
        """
            Check for any user input and execute
            any user definied macros for said inputs.
        """

        if not hasattr(self, 'macros'):
            return

        # Dequeue all current key events.
        while True:
            event = self.macropad.keys.events.get()

            # Break out when there are no more events.
            if not event:
                break

            # Check for for a key code.
            code = event.key_number
            if code != None:
                
                if event.pressed:
                    try:
                        self.macros.execute(str(code))
                    except Exception as e:
                        print_exception(e, e, e.__traceback__)

        # Track any change in the rotary encoder.
        rotary_current = self.macropad.encoder

        # Interpret positive/clockwise rotations as
        # volume up, negative/cc as volume down.
        if self.rotary_previous != rotary_current:

            if (self.rotary_previous - rotary_current) > 0:
                self.macros.execute('-')
            else:
                self.macros.execute('+')

        # Save current position for next cycle.
        self.rotary_previous = rotary_current


    def update(
        self,
        time_elapsed: float
    ):

        self.handle_inputs()

        if hasattr(self, 'leds'):
            self.leds.update_leds()

        if hasattr(self, 'display'):
            self.display.update(time_elapsed)