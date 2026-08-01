
def parse_str(value: str) -> RGBA:
    """Parse a string representing a color to an RGBA tuple.

    Possible formats for the input string include:

    * named color, see `COLORS_BY_NAME`
    * hex short eg. `<prefix>fff` (prefix can be `#`, `0x` or nothing)
    * hex long eg. `<prefix>ffffff` (prefix can be `#`, `0x` or nothing)
    * `rgb(<r>, <g>, <b>)`
    * `rgba(<r>, <g>, <b>, <a>)`

    Args:
        value: A string representing a color.

    Returns:
        An `RGBA` tuple parsed from the input string.

    Raises:
        ValueError: If the input string cannot be parsed to an RGBA tuple.
    """
    value_lower = value.lower()
    try:
        r, g, b = COLORS_BY_NAME[value_lower]
    except KeyError:
        pass
    else:
        return ints_to_rgba(r, g, b, None)

    m = re.fullmatch(r_hex_short, value_lower)
    if m:
        *rgb, a = m.groups()
        r, g, b = (int(v * 2, 16) for v in rgb)
        if a:
            alpha: Optional[float] = int(a * 2, 16) / 255
        else:
            alpha = None
        return ints_to_rgba(r, g, b, alpha)

    m = re.fullmatch(r_hex_long, value_lower)
    if m:
        *rgb, a = m.groups()
        r, g, b = (int(v, 16) for v in rgb)
        if a:
            alpha = int(a, 16) / 255
        else:
            alpha = None
        return ints_to_rgba(r, g, b, alpha)

    m = re.fullmatch(r_rgb, value_lower) or re.fullmatch(r_rgb_v4_style, value_lower)
    if m:
        return ints_to_rgba(*m.groups())  # type: ignore

    m = re.fullmatch(r_hsl, value_lower) or re.fullmatch(r_hsl_v4_style, value_lower)
    if m:
        return parse_hsl(*m.groups())  # type: ignore

    raise PydanticCustomError('color_error', 'value is not a valid color: string not recognised as a valid color')


def parse_str(value: str) -> RGBA:
    """
    Parse a string to an RGBA tuple, trying the following formats (in this order):
    * named color, see COLORS_BY_NAME below
    * hex short eg. `<prefix>fff` (prefix can be `#`, `0x` or nothing)
    * hex long eg. `<prefix>ffffff` (prefix can be `#`, `0x` or nothing)
    * `rgb(<r>, <g>, <b>) `
    * `rgba(<r>, <g>, <b>, <a>)`
    """
    value_lower = value.lower()
    try:
        r, g, b = COLORS_BY_NAME[value_lower]
    except KeyError:
        pass
    else:
        return ints_to_rgba(r, g, b, None)

    m = re.fullmatch(r_hex_short, value_lower)
    if m:
        *rgb, a = m.groups()
        r, g, b = (int(v * 2, 16) for v in rgb)
        if a:
            alpha: Optional[float] = int(a * 2, 16) / 255
        else:
            alpha = None
        return ints_to_rgba(r, g, b, alpha)

    m = re.fullmatch(r_hex_long, value_lower)
    if m:
        *rgb, a = m.groups()
        r, g, b = (int(v, 16) for v in rgb)
        if a:
            alpha = int(a, 16) / 255
        else:
            alpha = None
        return ints_to_rgba(r, g, b, alpha)

    m = re.fullmatch(r_rgb, value_lower)
    if m:
        return ints_to_rgba(*m.groups(), None)  # type: ignore

    m = re.fullmatch(r_rgba, value_lower)
    if m:
        return ints_to_rgba(*m.groups())  # type: ignore

    m = re.fullmatch(r_hsl, value_lower)
    if m:
        h, h_units, s, l_ = m.groups()
        return parse_hsl(h, h_units, s, l_)

    m = re.fullmatch(r_hsla, value_lower)
    if m:
        h, h_units, s, l_, a = m.groups()
        return parse_hsl(h, h_units, s, l_, parse_float_alpha(a))

    raise ColorError(reason='string not recognised as a valid color')

