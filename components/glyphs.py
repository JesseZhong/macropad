from adafruit_bitmap_font import bitmap_font
import re

class Glyphs:

    def __init__(
        self,
        filename: str = None
    ):
        if filename:
            self.font = bitmap_font.load_font(filename)

        else:
            self.font = None


    def cache(
        self,
        text: str
    ):
        def cache_unicode(
            match: re.Match
        ):
            unicode = match.group(1)

            try:
                # Attempt to cache.
                self.font.load_glyphs(unicode)
            except TypeError as e:
                print(e)

            return unicode

        if self.font:
            return re.sub(
                '([\uf000-\uffff])',
                cache_unicode,
                text
            )
