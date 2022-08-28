try:
    from typing import Dict, Tuple, Any, Callable
except ImportError:
    pass

from adafruit_macropad import MacroPad
from adafruit_led_animation.animation import Animation
from adafruit_led_animation.animation.solid import Solid
from components.ledanimation import LEDAnimation, DEFAULT_COLOR, DEFAULT_BRIGHTNESS


STARTING_ANIMATION_KEY = 'starting animation'

class LEDPixel:

    def __init__(
        self,
        data: Dict,
        macropad: MacroPad
    ):
        self.macropad = macropad

        # Localize LEDs.
        self.pixels = self.macropad.pixels

        self.animations: Dict[str, Animation] = {}
        
        # Load LED settings.
        if data:
                
            self.brightness = data['brightness'] if 'brightness' in data else DEFAULT_BRIGHTNESS
            self.pixels.brightness = self.brightness

            # Load animation configurations.
            if 'animations' in data:
                settings = data['animations']

                for setting_name, setting in settings.items():

                    # Safely get configuration values for an animation,
                    # using defaults when no values are provided
                    def get(
                        field: str,
                        cast: Callable[[Any], Any],
                        default: Any
                    ):
                        return cast(setting[field]) \
                            if field in setting \
                            else default

                    
                    if 'type' in setting:
                        anim_type = setting['type'].replace(' ', '_')

                        # Check if the animation type exists.
                        types = LEDAnimation.__dict__
                        if anim_type in types and callable(types[anim_type]):

                            # Load the animation, using any user defined values.
                            self.animations[setting_name] = types[anim_type](
                                self.pixels,
                                get
                            )


            # Set the starting, default animation.
            # Otherwise use solid as default.
            self.animation = self.animations[data[STARTING_ANIMATION_KEY]] \
                if STARTING_ANIMATION_KEY in data and data[STARTING_ANIMATION_KEY] in self.animations \
                else Solid(self.pixels, DEFAULT_COLOR)

        else:
            self.pixels.fill(DEFAULT_COLOR)
            self.brightness = DEFAULT_BRIGHTNESS
            self.pixels.brightness = self.brightness


    def update_leds(self):
        """
            Update the animations for the LEDs.
        """
        if hasattr(self, 'animation'):
            self.animation.animate()


    @property
    def on(self):
        """
            Indicate if the LEDs are on or off.
        """
        return self.pixels.brightness > 0


    @on.setter
    def on(
        self,
        value: bool
    ):
        """
            Set the LEDs on or off.
        """
        self.pixels.brightness = 0 if value else self.brightness


    def toggle(self):
        """
            Toggle the LEDs on or off.
        """
        self.pixels.brightness = 0 if self.pixels.brightness > 0 else self.brightness
