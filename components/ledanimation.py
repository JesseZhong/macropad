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