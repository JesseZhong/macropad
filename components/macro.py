try:
    from typing import Dict, List, Callable
except ImportError:
    pass

from adafruit_macropad import MacroPad
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.mouse import Mouse
from components.auxkeycodes import AuxKeyCode
from components.display import Display
from components.controller import Controller


class Macro:

    def __init__(
        self,
        macro_key: str,
        macropad: MacroPad,
        macro: Dict[str, str],
        display: Display,
        controller: Controller
    ):
        # Localize the key name.
        key = macro['key'] if 'key' in macro else None

        if key:
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
                    self.send_keys = lambda _: device.send(
                            type.__dict__[key],
                            *mods
                        )
                    break


        # Localize state changes.
        state = macro['state'] if 'state' in macro else None

        if state:
            tasks: List[Callable] = []

            if 'animation' in state:
                """Lookup"""

            if 'brightness' in state:
                """Value or +/-"""

            if 'led' in state:
                """
                    Allows for: true, false, 'toggle'
                """
                led = state['led']

                if led == 'toggle':
                    def toggle_led():
                        controller.pixel.toggle()
                        

                    tasks.append(toggle_led)

                else:
                    try:
                        led_value = bool(led)

                        def set_led():
                            controller.pixel.on = led_value

                        tasks.append(set_led)
                    except ValueError:
                        pass


            if 'lock' in state:
                """
                    Allows for: true, false, 'toggle'
                """
                lock = state['lock']

                if lock == 'toggle':
                    def toggle_lock():
                        controller.locked = not controller.locked

                    controller.add_lock_key(macro_key)

                    tasks.append(toggle_lock)

                else:
                    try:
                        lock_value = bool(lock)

                        def set_lock():
                            controller.locked = lock_value

                        controller.add_lock_key(macro_key)

                        tasks.append(set_lock)
                    except ValueError:
                        pass


            def alter_state():
                for task in tasks:
                    task()

            self.alter_state = alter_state

        # Load any messages to show when the key is pressed.
        message = macro['message'] if 'message' in macro else None
        if message:
            self.display_message = lambda _: display.write(message)


    def execute(self):
        """
            Send key to receiving device,
            change macropad state,
            and/or display a message if available.
        """
        
        if hasattr(self, 'send_keys'):
            self.send_keys(None)

        if hasattr(self, 'alter_state'):
            self.alter_state()

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
        display: Display,
        controller: Controller
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
            display,
            controller
        )

        # Import modified macros.
        self.modified_macros: Dict[str, Macro] = self.process_data(
            modified_data,
            macropad,
            display,
            controller
        )

    def process_data(
        self,
        data: Dict[str, Macro],
        macropad: MacroPad,
        display: Display,
        controller: Controller
    ):
        result: Dict[str, Macro] = {}

        if data:
            for macro_key, macro_config in data.items():
                result[macro_key] = Macro(
                    macro_key,
                    macropad,
                    macro_config,
                    display,
                    controller
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
            self.modified_macros[key].execute()

        elif not modified and key in self.macros:
            self.macros[key].execute()