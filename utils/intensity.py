
def intensity(c, i):
    """Return color c changed by intensity i

    For 0 <= i <= 127 the color is a shade, with 0 being black, 127 being the
    unaltered color.

    For 128 <= i <= 255 the color is a tint, with 255 being white, 128 the
    unaltered color.

    """
    r, g, b = c[0:3]
    if 0 <= i <= 127:
        # Darken
        return ((r * i) // 127, (g * i) // 127, (b * i) // 127)
    # Lighten
    return (
        r + ((255 - r) * (255 - i)) // 127,
        g + ((255 - g) * (255 - i)) // 127,
        b + ((255 - b) * (255 - i)) // 127,
    )

