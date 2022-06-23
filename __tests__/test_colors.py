import unittest
from components.colors import Colors

class TestColors(unittest.TestCase):

    def test_parse_names(self):
        
        names = {
            'RED': (255, 0, 0),
            'GREEN': (0, 128, 0),
            'GOLD': (255, 215, 0),
            'WHITE': (255, 255, 255),
            'dark GOLDEN Rod': (184, 134, 11),
            'Medium Spring Green': (0, 250, 154)
        }

        for name, expected in names.items():
            actual = Colors.parse(name)

            self.assertEqual(
                actual,
                expected,
                f'Expected {expected} for {name}, but got {actual} instead.'
            )


    def test_parse_hexcode(self):

        hexcodes = {
            '#000000': (0, 0, 0),
            '#1C1C1C': (28, 28, 28),
            '#641C34': (100, 28, 52),
            '#008F39': (0, 143, 57),
            '#102C54': (16, 44, 84)
        }

        for code, expected in hexcodes.items():
            actual = Colors.parse(code)

            self.assertEqual(
                actual,
                expected,
                f'Expected {expected} for {code}, but got {actual} instead.'
            )
