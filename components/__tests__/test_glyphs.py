import unittest
from unittest.mock import patch
from components.glyphs import Glyphs

class TestGlyphs(unittest.TestCase):

    @patch('adafruit_bitmap_font.bitmap_font.load_font')
    def test_normalization(
        self,
        wrapped_load_font
    ):
        text_to_expected_cache = {
            '\uf04b\uf04c': 2,
            'Join us on \uf2ee.': 1,
            'Minecraft is \uf10dREAL\uf10e, don\'t you know\uf128': 3
        }

        for text, expected in text_to_expected_cache.items():
            glyphs = Glyphs('fake')

            with patch.object(
                glyphs,
                'font'
            ) as wrapped_load_glyphs:

                glyphs.cache(text)

                actual = wrapped_load_glyphs.load_glyphs.call_count

                self.assertEqual(
                    actual,
                    expected,
                    f'Number of cached.\n\tActual: {actual}\n\tExpected: {expected}'
                )