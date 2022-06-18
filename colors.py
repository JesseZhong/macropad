from re import match


class Colors:

    @classmethod
    def parse(
        cls,
        value
    ):
        if not value or not isinstance(value, str):
            raise ValueError('Color value must be a valid string.')

        # All the way up!
        value = value.upper()

        # Check if it's in hex format.
        if match(
            r'#[0-9A-F]{6}',
            value
        ):
            red = int(value[1:2], base=16)
            green = int(value[3:4], base=16)
            blue = int(value[5:6], base=16)

            return (red, green, blue)

        # Check if it's one of the predefined colors.
        elif value in cls.__dict__:

            return cls.__dict__[value]

        else:
            raise ValueError('Unknown color.')