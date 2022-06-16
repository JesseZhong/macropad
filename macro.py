try:
    from typing import Dict
except ImportError:
    pass

from adafruit_macropad import MacroPad
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.mouse import Mouse
from json import load


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

        # Localize any key modifiers and get their key codes.
        mods = [Keycode.__dict__[k] for k in macro['mods']] \
            if 'mods' in macro and isinstance(macro['mods'], list) \
            else []
        
        # Locate the corresponding keycode to specified key name.
        if hasattr(Keycode, key):
            self.handle = lambda _: macropad.keyboard.send(
                Keycode.__dict__[key],
                *mods
            )

        elif hasattr(ConsumerControlCode, key):
            self.handle = lambda _: macropad.consumer_control.send(
                ConsumerControlCode.__dict__[key],
                *mods
            )

        elif hasattr(Mouse, key):
            self.handle = lambda _: macropad.mouse.send(
                Mouse.__dict__[key],
                *mods
            )

        message = macro['message'] if 'message' in macro else None
        if message:
            self.display_message = lambda _: macropad.display_text(message)


    def send(self):
        """
            Send key to receiving device and
            display a message if available.
        """
        
        if hasattr(self, 'handle'):
            self.handle(None)

            if hasattr(self, 'display_message'):
                self.display_message(None)


class Macros:
    """
        Loads, stores, and executes user-defined macros.
    """

    def __init__(
        self,
        config_file: str,
        macropad: MacroPad
    ):
        """
            Loads all of the user macros from the file.

            Parameters
            ----------
            config_file : str
                Name of the config file that contains all the macros.
            macropad : MacroPad
                Macro pad object used to handle user inputs and execute macros.
        """

        # Import macros.
        self.macros: Dict[str, Macro] = {}

        with open(
            config_file,
            'rt',
            encoding='UTF-8'
        ) as file:
            data: Dict = load(file)

            if data:
                for macro_key, macro_config in data.items():
                    self.macros[macro_key] = Macro(
                        macropad,
                        macro_config
                    )


    def execute(
        self,
        key: str
    ):
        """
            Check if a key has a defined macro for it.
            Execute the macro if it does.
        """
        if key in self.macros:
            self.macros[key].send()