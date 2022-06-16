try:
    from typing import Dict
except ImportError:
    pass

from adafruit_macropad import MacroPad
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.mouse import Mouse


class Macro:

    def __init__(
        self,
        macropad: MacroPad,
        macro: Dict[str, str]
    ):
        # Localize the key name.
        key = macro['key'] if 'key' in macro else None
        if not key:
            return
        
        # Locate the corresponding keycode to specified key name.
        if hasattr(Keycode, key):
            self.handle = lambda _: macropad.keyboard.send(Keycode.__dict__[key])

        elif hasattr(ConsumerControlCode, key):
            self.handle = lambda _: macropad.consumer_control.send(ConsumerControlCode.__dict__[key])

        elif hasattr(Mouse, key):
            self.handle = lambda _: macropad.mouse.send(Mouse.__dict__[key])

        message = macro['message'] if 'message' in macro else None
        if message:
            self.display_message = lambda _: macropad.display_text(message)


    def send(self):
        """
            Send key to receiving device and
            display a message if available.
        """
        
        if hasattr(self, 'handle'):
            self.handle()

            if hasattr(self, 'display_message'):
                self.display_message()