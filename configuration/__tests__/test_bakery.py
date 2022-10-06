import unittest
from configuration.bakery import Bakery

class TestBakery(unittest.TestCase):

    def test_bake_glyphs(self):

        text = {
            'f{play}f{pause}': '\uf04b\uf04c',
            'Join us on f{discord}.': 'Join us on \uf2ee.',
            'Minecraft is f{quote left}REALf{quote right}, don\'t you knowf{question}': 'Minecraft is \uf10dREAL\uf10e, don\'t you know\uf128'
        }

        bakery = Bakery(
            input_config='',
            output_dir=''
        )

        for original, expected in text.items():
            actual = bakery.bake_glyphs(original)

            self.assertEqual(
                actual,
                expected,
                f'Text doesn\' match.\n\tActual: {actual}\n\tExpected: {expected}'
            )