
def parse_hsl(h: str, h_units: str, sat: str, light: str, alpha: Optional[float] = None) -> RGBA:
    """Parse raw hue, saturation, lightness, and alpha values and convert to RGBA.

    Args:
        h: The hue value.
        h_units: The unit for hue value.
        sat: The saturation value.
        light: The lightness value.
        alpha: Alpha value.

    Returns:
        An instance of `RGBA`.
    """
    s_value, l_value = parse_color_value(sat, 100), parse_color_value(light, 100)

    h_value = float(h)
    if h_units in {None, 'deg'}:
        h_value = h_value % 360 / 360
    elif h_units == 'rad':
        h_value = h_value % rads / rads
    else:
        # turns
        h_value = h_value % 1

    r, g, b = hls_to_rgb(h_value, l_value, s_value)
    return RGBA(r, g, b, parse_float_alpha(alpha))


def parse_hsl(h: str, h_units: str, sat: str, light: str, alpha: Optional[float] = None) -> RGBA:
    """
    Parse raw hue, saturation, lightness and alpha values and convert to RGBA.
    """
    s_value, l_value = parse_color_value(sat, 100), parse_color_value(light, 100)

    h_value = float(h)
    if h_units in {None, 'deg'}:
        h_value = h_value % 360 / 360
    elif h_units == 'rad':
        h_value = h_value % rads / rads
    else:
        # turns
        h_value = h_value % 1

    r, g, b = hls_to_rgb(h_value, l_value, s_value)
    return RGBA(r, g, b, alpha)

