try:
    from typing import Dict
except ImportError:
    pass

from adafruit_macropad import MacroPad
from traceback import print_exception
from json import load
from components.controller import Controller
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
        self.controller = Controller()

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
                    data['modified_macros'] if 'modified_macros' in data else None,
                    self.macropad,
                    self.display,
                    self.controller
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

        # Toggle LEDs. DO NOT localize switch, as state changes aren't tracked.
        # TODO: Move all this to LED module.
        self.macropad.encoder_switch_debounced.update()

        # Dequeue all current key events.
        while True:
            event = self.macropad.keys.events.get()

            # Break out when there are no more events.
            if not event:
                break

            # Check for for a key code.
            key_number = event.key_number
            if key_number != None:

                if event.pressed and (
                    not self.controller.locked or \
                    self.controller.is_lock_key(str(key_number))
                ):
                    try:
                        self.macros.execute(
                            str(key_number),
                            not self.macropad.encoder_switch_debounced.value
                        )
                    except Exception as e:
                        print_exception(e, e, e.__traceback__)

        # Track any change in the rotary encoder.
        rotary_current = self.macropad.encoder

        # Interpret positive/clockwise rotations as
        # volume up, negative/cc as volume down.
        if self.rotary_previous != rotary_current:

            if (self.rotary_previous - rotary_current) > 0:
                self.macros.execute(
                    '-',
                    self.macropad.encoder_switch_debounced.pressed
                )
            else:
                self.macros.execute(
                    '+',
                    self.macropad.encoder_switch_debounced.pressed
                )

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