try:
    from typing import Dict
except ImportError:
    pass

from adafruit_macropad import MacroPad


class LEDPixel:

    def __init__(
        self,
        data: Dict,
        macropad: MacroPad
    ):
        self.macropad = macropad

        # Localize LEDs.
        self.pixels = self.macropad.pixels

        # TODO: Actually do something with this.
        self.brightness = 1.0


    def process_leds(
        self,
        time_elapsed: float
    ):
        """
        """

        # Toggle LEDs. DO NOT localize switch, as state changes aren't tracked.
        # TODO: Move all this to LED module.
        self.macropad.encoder_switch_debounced.update()
        if self.macropad.encoder_switch_debounced.released:

            self.pixels.brightness = 0 if self.pixels.brightness > 0 else self.brightness
