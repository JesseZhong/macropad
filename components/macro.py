try:
    from typing import Dict
except ImportError:
    pass

from adafruit_macropad import MacroPad
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.mouse import Mouse
from components.auxkeycodes import AuxKeyCode
from components.display import Display


class Macro:

    def __init__(
        self,
        macropad: MacroPad,
        macro: Dict[str, str],
        display: Display
    ):
        # Localize the key name.
        key = macro['key'] if 'key' in macro else None
        if not key or not isinstance(key, str):
            raise ValueError('Invalid key.')

        key = key.upper()

        # Localize any key modifiers and get their key codes.
        mods = [Keycode.__dict__[k] for k in macro['mods']] \
            if 'mods' in macro and isinstance(macro['mods'], list) \
            else []

        macroTypes = {
            Keycode: macropad.keyboard,

            # Adafruit definited consumer control key.
            ConsumerControlCode: macropad.consumer_control,

            # Auxiliary list of supported keys.
            AuxKeyCode: macropad.keyboard,

            # Mouse buttons?
            Mouse: macropad.mouse
        }

        # Locate the corresponding keycode to specified key name.
        for type, device in macroTypes.items():
            if hasattr(type, key):
                self.handle = lambda _: device.send(
                        type.__dict__[key],
                        *mods
                    )
                break

        # Load any messages to show when the key is pressed.
        message = macro['message'] if 'message' in macro else None
        if message:
            self.display_message = lambda _: display.write(message)


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
        data: Dict[str, Macro],
        modified_data: Dict[str, Macro],
        macropad: MacroPad,
        display: Display
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
        self.macros: Dict[str, Macro] = self.process_data(
            data,
            macropad,
            display
        )

        # Import modified macros.
        self.modified_macros: Dict[str, Macro] = self.process_data(
            modified_data,
            macropad,
            display
        )

    def process_data(
        self,
        data: Dict[str, Macro],
        macropad: MacroPad,
        display: Display
    ):
        result: Dict[str, Macro] = {}

        if data:
            for macro_key, macro_config in data.items():
                result[macro_key] = Macro(
                    macropad,
                    macro_config,
                    display
                )

        return result


    def execute(
        self,
        key: str,
        modified: bool
    ):
        """
            Check if a key has a defined macro for it.
            Execute the macro if it does.
        """
        if modified and key in self.modified_macros:
            self.modified_macros[key].send()

        elif key in self.macros:
            self.macros[key].send()