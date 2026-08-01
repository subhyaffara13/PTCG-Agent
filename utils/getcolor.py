
def getcolor(color: str, mode: str) -> int | tuple[int, ...]:
    """
    Same as :py:func:`~PIL.ImageColor.getrgb` for most modes. However, if
    ``mode`` is HSV, converts the RGB value to a HSV value, or if ``mode`` is
    not color or a palette image, converts the RGB value to a grayscale value.
    If the string cannot be parsed, this function raises a :py:exc:`ValueError`
    exception.

    .. versionadded:: 1.1.4

    :param color: A color string
    :param mode: Convert result to this mode
    :return: ``graylevel, (graylevel, alpha) or (red, green, blue[, alpha])``
    """
    # same as getrgb, but converts the result to the given mode
    rgb, alpha = getrgb(color), 255
    if len(rgb) == 4:
        alpha = rgb[3]
        rgb = rgb[:3]

    if mode == "HSV":
        from colorsys import rgb_to_hsv

        r, g, b = rgb
        h, s, v = rgb_to_hsv(r / 255, g / 255, b / 255)
        return int(h * 255), int(s * 255), int(v * 255)
    elif Image.getmodebase(mode) == "L":
        r, g, b = rgb
        # ITU-R Recommendation 601-2 for nonlinear RGB
        # scaled to 24 bits to match the convert's implementation.
        graylevel = (r * 19595 + g * 38470 + b * 7471 + 0x8000) >> 16
        if mode[-1] == "A":
            return graylevel, alpha
        return graylevel
    elif mode[-1] == "A":
        return rgb + (alpha,)
    return rgb

