from adafruit_macropad import MacroPad
from traceback import print_exception
from macro import Macros


class MacroPadManager:

    def __init__(
        self,
        macropad: MacroPad
    ):
        self.macropad = macropad

        # Load and setup macros.
        self.macros = Macros(
            './config.json',
            self.macropad
        )

        # Track the initial state of the rotary encoder.
        self.rotary_previous = macropad.encoder


    def handle_inputs(self):
        """
            Check for any user input and execute
            any user definied macros for said inputs.
        """

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

        self.rotary_previous = rotary_current