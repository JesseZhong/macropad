import unittest
from components.glyphs import Glyphs

class TestGlyphs(unittest.TestCase):

    def test_normalization(self):

        text = {
            'f{play}f{pause}': '\uf04b\uf04c',
            'Join us on f{discord}.': 'Join us on \uf2ee.',
            'Minecraft is f{quote_left}REALf{quote_right}, don\'t you knowf{question}': 'Minecraft is \uf10dREAL\uf10e, don\'t you know\uf128'
        }

        glyphs = Glyphs()

        for original, expected in text.items():
            actual = glyphs.normalize(original)

            self.assertEqual(
                actual,
                expected,
                f'Text doesn\' match.\n\tActual: {actual}\n\tExpected: {expected}'
            )