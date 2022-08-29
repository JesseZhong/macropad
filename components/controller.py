try:
    from typing import Set
except ImportError:
    pass

from components.ledpixel import LEDPixel


class Controller:

    def __init__(
        self,
        pixel: LEDPixel
    ):
        self._lock_keys: Set[str] = set()
        self._locked = False

        self.pixel = pixel


    def add_lock_key(
        self,
        key: str
    ):
        self._lock_keys.add(key)


    def is_lock_key(
        self,
        key: str
    ):
        return key in self._lock_keys


    @property
    def locked(self):
        return self._locked


    @locked.setter
    def locked(
        self,
        value: bool
    ):
        self._locked = value