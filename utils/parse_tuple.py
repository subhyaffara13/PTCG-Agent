
def parse_tuple(value: tuple[Any, ...]) -> RGBA:
    """Parse a tuple or list to get RGBA values.

    Args:
        value: A tuple or list.

    Returns:
        An `RGBA` tuple parsed from the input tuple.

    Raises:
        PydanticCustomError: If tuple is not valid.
    """
    if len(value) == 3:
        r, g, b = (parse_color_value(v) for v in value)
        return RGBA(r, g, b, None)
    elif len(value) == 4:
        r, g, b = (parse_color_value(v) for v in value[:3])
        return RGBA(r, g, b, parse_float_alpha(value[3]))
    else:
        raise PydanticCustomError('color_error', 'value is not a valid color: tuples must have length 3 or 4')


def parse_tuple(value: Tuple[Any, ...]) -> RGBA:
    """
    Parse a tuple or list as a color.
    """
    if len(value) == 3:
        r, g, b = (parse_color_value(v) for v in value)
        return RGBA(r, g, b, None)
    elif len(value) == 4:
        r, g, b = (parse_color_value(v) for v in value[:3])
        return RGBA(r, g, b, parse_float_alpha(value[3]))
    else:
        raise ColorError(reason='tuples must have length 3 or 4')

