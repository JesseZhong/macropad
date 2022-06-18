try:
    from typing import Dict
except ImportError:
    pass

from adafruit_macropad import MacroPad


MESSAGE_TIMEOUT = 2.0


class Display:

    def __init__(
        self,
        data: Dict,
        macropad: MacroPad
    ):
        def get(
            property_name: str,
            default: str = None
        ):
            return data[property_name] \
                if data and property_name in data \
                else default

        self.title = get('title')
        self.title_scale = get('title_scale')
        self.message_timeout = get(
            'message_timeout',
            MESSAGE_TIMEOUT
        )

        self.macropad = macropad
        self.clear()


    def clear(
        self
    ):
        self.text_display = self.macropad.display_text(
            title=self.title,
            title_scale=self.title_scale
        )
        self.written = False
        self.timeout = 0
        self.text_display.show()

    
    def write(
        self,
        message: str
    ):
        self.text_display[0].text = message
        self.written = True
        self.timeout = MESSAGE_TIMEOUT
        self.text_display.show()


    def update(
        self,
        elapsed_time: float
    ):
        self.timeout = max(0, self.timeout - elapsed_time)

        if self.written and self.timeout <= 0:
            self.clear()