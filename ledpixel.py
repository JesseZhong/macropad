try:
    from typing import Dict
except ImportError:
    pass

from adafruit_macropad import MacroPad
import adafruit_led_animation.animation as anim


DEFAULT_COLOR = (255, 255, 255)
DEFAULT_BRIGHTNESS = 1.0

class LEDPixel:

    def __init__(
        self,
        data: Dict,
        macropad: MacroPad
    ):
        self.macropad = macropad

        # Localize LEDs.
        self.pixels = self.macropad.pixels

        if data:

            if 'solid' in data:

                solid = data['solid']
                
                self.pixels.fill(
                    solid['color'] \
                    if 'color' in solid \
                    else DEFAULT_COLOR
                )

                self.brightness = float(solid['brightness']) \
                    if 'brightness' in solid \
                    else DEFAULT_BRIGHTNESS
                
                self.pixels.brightness = self.brightness

        else:
            self.pixels.fill(DEFAULT_COLOR)
            self.brightness = DEFAULT_BRIGHTNESS
            self.pixels.brightness = self.brightness


    def update_leds(
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
