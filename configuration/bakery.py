from configuration.glyphkeys import GLYPH_KEYS
from os.path import splitext, join, basename
from json import loads, dump
import re


class Bakery:

    def __init__(
        self,
        input_config: str,
        output_dir: str
    ):
        self.input = input_config
        self.output = output_dir

    def bake(self):
        """"""
        [
            name,
            ext
        ] = splitext(basename(self.input))

        outpath = join(self.output, f'{name}.baked{ext}')

        result = ''
        with open(self.input, 'r') as f:
            result = self.bake_glyphs(f.read())

        if result:
            with open(outpath, 'w') as f:
                self.write_minified(f, result)
                print(f'Baked {self.input}. Output: {outpath}')


    def bake_glyphs(
        self,
        text: str
    ):
        def key_replace(
            match: re.Match
        ):
            if not match:
                return ''

            key = match.group(1).lower()

            return GLYPH_KEYS[key] if key in GLYPH_KEYS else ''

        return re.sub(
            r'f{([a-zA-Z0-9 ]+)}',
            key_replace,
            text
        )

    def write_minified(
        self,
        fobject,
        text: str
    ):
        data = loads(text)
        dump(data,
            fobject,
            separators=(',', ':')
        )


if __name__ == '__main__':
    bakery = Bakery(
        './config.json',
        './'
    )

    bakery.bake()