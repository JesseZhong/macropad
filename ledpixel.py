try:
    from typing import Dict, Any, Callable
except ImportError:
    pass

from adafruit_macropad import MacroPad
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from colors import Colors


DEFAULT_COLOR = (255, 255, 255)
DEFAULT_BRIGHTNESS = 1.0
DEFAULT_SPEED = 0.1

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

            def fetch(obj_name: str):
                def get(
                    field: str,
                    cast: Callable[[Any], Any],
                    default: Any
                ):
                    return cast(data[obj_name][field]) \
                        if field in data[obj_name] \
                        else default

                return get

            
            self.brightness = data['brightness'] if 'brightness' in data else DEFAULT_BRIGHTNESS
            self.pixels.brightness = self.brightness

            if 'solid' in data:

                solid = fetch('solid')

                self.animation = Solid(
                    self.pixels,
                    solid('color', Colors.parse, DEFAULT_COLOR)
                )

            elif 'rainbow' in data:

                rb = fetch('rainbow')

                self.animation = Rainbow(
                    self.pixels,
                    rb('speed', float, DEFAULT_SPEED),
                    rb('period', float, 5.0)
                )

            elif 'rainbow chase' in data:

                rbc = fetch('rainbow chase')

                self.animation = RainbowChase(
                    self.pixels,
                    rbc('speed', float, DEFAULT_SPEED),
                    size=rbc('size', int, 2),
                    spacing=rbc('spacing', int, 3),
                    reverse=rbc('reverse', bool, False),
                    step=rbc('step', int, 8)
                )

            elif 'rainbow comet' in data:

                rbc = fetch('rainbow comet')

                self.animation = RainbowComet(
                    self.pixels,
                    rbc('speed', float, DEFAULT_SPEED),
                    tail_length=rbc('tail length', int, 10),
                    reverse=rbc('reverse', bool, False),
                    bounce=rbc('bounce', bool, False),
                    ring=rbc('ring', bool, False)
                )

            elif 'rainbow sparkle' in data:

                rbs = fetch('rainbow sparkle')

                self.animation = RainbowSparkle(
                    self.pixels,
                    rbs('speed', float, DEFAULT_SPEED),
                    period=rbs('period', float, 5.0),
                    num_sparkles=rbs('sparkles', int, None),
                    step=rbs('step', int, 1)
                )

            elif 'blink' in data:

                blink = fetch('blink')

                self.animation = Blink(
                    self.pixels,
                    blink('speed', float, DEFAULT_SPEED),
                    blink('color', Colors.parse, DEFAULT_COLOR)
                )

            elif 'pulse' in data:

                pulse = fetch('pulse')

                self.animation = Pulse(
                    self.pixels,
                    pulse('speed', float, DEFAULT_SPEED),
                    pulse('color', Colors.parse, DEFAULT_COLOR),
                    period=pulse('period', float, 5.0)
                )

            elif 'sparkle pulse' in data:

                sp = fetch('sparkle pulse')

                self.animation = SparklePulse(
                    self.pixels,
                    sp('speed', float, DEFAULT_SPEED),
                    sp('color', Colors.parse, DEFAULT_COLOR),
                    sp('period', float, 5.0),
                    sp('max intensity', float, 1.0),
                    sp('min intensity', float, 0)
                )

        else:
            self.pixels.fill(DEFAULT_COLOR)
            self.brightness = DEFAULT_BRIGHTNESS
            self.pixels.brightness = self.brightness


    def update_leds(self):
        """
            Update the animations for the LEDs.
        """

        # Toggle LEDs. DO NOT localize switch, as state changes aren't tracked.
        # TODO: Move all this to LED module.
        self.macropad.encoder_switch_debounced.update()
        if self.macropad.encoder_switch_debounced.released:

            self.pixels.brightness = 0 if self.pixels.brightness > 0 else self.brightness

        if hasattr(self, 'animation'):
            self.animation.animate()