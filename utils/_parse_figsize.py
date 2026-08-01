
def _parse_figsize(figsize, dpi):
    """
    Convert a figsize expression to (width, height) in inches.

    Parameters
    ----------
    figsize : (float, float) or (float, float, str)
        This can be

        - a tuple ``(width, height, unit)``, where *unit* is one of "in" (inch),
          "cm" (centimenter), "px" (pixel).
        - a tuple ``(width, height)``, which is interpreted in inches, i.e. as
          ``(width, height, "in")``.

    dpi : float
        The dots-per-inch; used for converting 'px' to 'in'.
    """
    num_parts = len(figsize)
    if num_parts == 2:
        x, y = figsize
    elif num_parts == 3:
        x, y, unit = figsize
        if unit == 'in':
            pass
        elif unit == 'cm':
            if x is not None:
                x /= 2.54
            if y is not None:
                y /= 2.54
        elif unit == 'px':
            if x is not None:
                x /= dpi
            if y is not None:
                y /= dpi
        else:
            raise ValueError(
                f"Invalid unit {unit!r} in 'figsize'; "
                "supported units are 'in', 'cm', 'px'"
            )
    else:
        raise ValueError(
            "Invalid figsize format, expected (x, y) or (x, y, unit) but got "
            f"{figsize!r}"
        )

    if x is None and y is None:
        raise ValueError(
            "figsize=(None, None) is invalid; at least one of width or "
            "height must be provided")

    default_width, default_height = mpl.rcParams["figure.figsize"]
    if x is None:
        x = default_width
    if y is None:
        y = default_height
    return x, y

