
def colorize(
    image: Image.Image,
    black: str | tuple[int, ...],
    white: str | tuple[int, ...],
    mid: str | int | tuple[int, ...] | None = None,
    blackpoint: int = 0,
    whitepoint: int = 255,
    midpoint: int = 127,
) -> Image.Image:
    """
    Colorize grayscale image.
    This function calculates a color wedge which maps all black pixels in
    the source image to the first color and all white pixels to the
    second color. If ``mid`` is specified, it uses three-color mapping.
    The ``black`` and ``white`` arguments should be RGB tuples or color names;
    optionally you can use three-color mapping by also specifying ``mid``.
    Mapping positions for any of the colors can be specified
    (e.g. ``blackpoint``), where these parameters are the integer
    value corresponding to where the corresponding color should be mapped.
    These parameters must have logical order, such that
    ``blackpoint <= midpoint <= whitepoint`` (if ``mid`` is specified).

    :param image: The image to colorize.
    :param black: The color to use for black input pixels.
    :param white: The color to use for white input pixels.
    :param mid: The color to use for midtone input pixels.
    :param blackpoint: an int value [0, 255] for the black mapping.
    :param whitepoint: an int value [0, 255] for the white mapping.
    :param midpoint: an int value [0, 255] for the midtone mapping.
    :return: An image.
    """

    # Initial asserts
    assert image.mode == "L"
    if mid is None:
        assert 0 <= blackpoint <= whitepoint <= 255
    else:
        assert 0 <= blackpoint <= midpoint <= whitepoint <= 255

    # Define colors from arguments
    rgb_black = cast(Sequence[int], _color(black, "RGB"))
    rgb_white = cast(Sequence[int], _color(white, "RGB"))
    rgb_mid = cast(Sequence[int], _color(mid, "RGB")) if mid is not None else None

    # Empty lists for the mapping
    red = []
    green = []
    blue = []

    # Create the low-end values
    for i in range(blackpoint):
        red.append(rgb_black[0])
        green.append(rgb_black[1])
        blue.append(rgb_black[2])

    # Create the mapping (2-color)
    if rgb_mid is None:
        range_map = range(whitepoint - blackpoint)

        for i in range_map:
            red.append(
                rgb_black[0] + i * (rgb_white[0] - rgb_black[0]) // len(range_map)
            )
            green.append(
                rgb_black[1] + i * (rgb_white[1] - rgb_black[1]) // len(range_map)
            )
            blue.append(
                rgb_black[2] + i * (rgb_white[2] - rgb_black[2]) // len(range_map)
            )

    # Create the mapping (3-color)
    else:
        range_map1 = range(midpoint - blackpoint)
        range_map2 = range(whitepoint - midpoint)

        for i in range_map1:
            red.append(
                rgb_black[0] + i * (rgb_mid[0] - rgb_black[0]) // len(range_map1)
            )
            green.append(
                rgb_black[1] + i * (rgb_mid[1] - rgb_black[1]) // len(range_map1)
            )
            blue.append(
                rgb_black[2] + i * (rgb_mid[2] - rgb_black[2]) // len(range_map1)
            )
        for i in range_map2:
            red.append(rgb_mid[0] + i * (rgb_white[0] - rgb_mid[0]) // len(range_map2))
            green.append(
                rgb_mid[1] + i * (rgb_white[1] - rgb_mid[1]) // len(range_map2)
            )
            blue.append(rgb_mid[2] + i * (rgb_white[2] - rgb_mid[2]) // len(range_map2))

    # Create the high-end values
    for i in range(256 - whitepoint):
        red.append(rgb_white[0])
        green.append(rgb_white[1])
        blue.append(rgb_white[2])

    # Return converted image
    image = image.convert("RGB")
    return _lut(image, red + green + blue)


def colorize(color_key, text):
    return codes[color_key] + text + codes["reset"]


def colorize(color_key, text):
    return codes[color_key] + text + codes["reset"]


def colorize(
    string: str, color: str, bold: bool = False, highlight: bool = False
) -> str:
    """Returns string surrounded by appropriate terminal colour codes to print colourised text.

    Args:
        string: The message to colourise
        color: Literal values are gray, red, green, yellow, blue, magenta, cyan, white, crimson
        bold: If to bold the string
        highlight: If to highlight the string

    Returns:
        Colourised string
    """
    attr = []
    num = color2num[color]
    if highlight:
        num += 10
    attr.append(str(num))
    if bold:
        attr.append("1")
    attrs = ";".join(attr)
    return f"\x1b[{attrs}m{string}\x1b[0m"


def colorize(
    string: str, color: str, bold: bool = False, highlight: bool = False
) -> str:
    """Returns string surrounded by appropriate terminal colour codes to print colourised text.

    Args:
        string: The message to colourise
        color: Literal values are gray, red, green, yellow, blue, magenta, cyan, white, crimson
        bold: If to bold the string
        highlight: If to highlight the string

    Returns:
        Colourised string
    """
    attr = []
    num = color2num[color]
    if highlight:
        num += 10
    attr.append(str(num))
    if bold:
        attr.append("1")
    attrs = ";".join(attr)
    return f"\x1b[{attrs}m{string}\x1b[0m"

