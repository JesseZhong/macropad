try:
    from typing import Dict, Tuple, Any, Callable
except ImportError:
    pass

from adafruit_macropad import MacroPad
from adafruit_led_animation.animation import Animation
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from components.colors import Colors


DEFAULT_COLOR = (255, 255, 255)
DEFAULT_BRIGHTNESS = 1.0
DEFAULT_SPEED = 0.1


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


class LEDAnimation:

    def solid(
        pixels,
        solid
    ):
        return Solid(
            pixels,
            solid('color', Colors.parse, DEFAULT_COLOR)
        )


    def rainbow(
        pixels,
        rb
    ):
        return Rainbow(
            pixels,
            rb('speed', float, DEFAULT_SPEED),
            rb('period', float, 5.0)
        )


    def rainbow_chase(
        pixels,
        rbc
    ):
        return RainbowChase(
            pixels,
            rbc('speed', float, DEFAULT_SPEED),
            size=rbc('size', int, 2),
            spacing=rbc('spacing', int, 3),
            reverse=rbc('reverse', bool, False),
            step=rbc('step', int, 8)
        )


    def rainbow_comet(
        pixels,
        rbc
    ):
        return RainbowComet(
            pixels,
            rbc('speed', float, DEFAULT_SPEED),
            tail_length=rbc('tail length', int, 10),
            reverse=rbc('reverse', bool, False),
            bounce=rbc('bounce', bool, False),
            ring=rbc('ring', bool, False)
        )


    def rainbow_sparkle(
        pixels,
        rbs
    ):
        return RainbowSparkle(
            pixels,
            rbs('speed', float, DEFAULT_SPEED),
            period=rbs('period', float, 5.0),
            num_sparkles=rbs('sparkles', int, None),
            step=rbs('step', int, 1)
        )


    def blink(
        pixels,
        blink
    ):
        return Blink(
            pixels,
            blink('speed', float, DEFAULT_SPEED),
            blink('color', Colors.parse, DEFAULT_COLOR)
        )


    def pulse(
        pixels,
        pulse
    ):
        return Pulse(
            pixels,
            pulse('speed', float, DEFAULT_SPEED),
            pulse('color', Colors.parse, DEFAULT_COLOR),
            period=pulse('period', float, 5.0)
        )


    def sparkle_pulse(
        pixels,
        sp
    ):
        return SparklePulse(
            pixels,
            sp('speed', float, DEFAULT_SPEED),
            sp('color', Colors.parse, DEFAULT_COLOR),
            sp('period', float, 5.0),
            sp('max intensity', float, 1.0),
            sp('min intensity', float, 0)
        )