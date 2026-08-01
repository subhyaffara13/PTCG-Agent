
def _is_single_string_color(color: Color) -> bool:
    """Check if `color` is a single string color.

    Examples of single string colors:
        - 'r'
        - 'g'
        - 'red'
        - 'green'
        - 'C3'
        - 'firebrick'

    Parameters
    ----------
    color : Color
        Color string or sequence of floats.

    Returns
    -------
    bool
        True if `color` looks like a valid color.
        False otherwise.
    """
    conv = matplotlib.colors.ColorConverter()
    try:
        # error: Argument 1 to "to_rgba" of "ColorConverter" has incompatible type
        # "str | Sequence[float]"; expected "tuple[float, float, float] | ..."
        conv.to_rgba(color)  # type: ignore[arg-type]
    except ValueError:
        return False
    else:
        return True

