
def _is_single_color(color: Color | Collection[Color]) -> bool:
    """Check if `color` is a single color, not a sequence of colors.

    Single color is of these kinds:
        - Named color "red", "C0", "firebrick"
        - Alias "g"
        - Sequence of floats, such as (0.1, 0.2, 0.3) or (0.1, 0.2, 0.3, 0.4).

    See Also
    --------
    _is_single_string_color
    """
    if isinstance(color, str) and _is_single_string_color(color):
        # GH #36972
        return True

    if _is_floats_color(color):
        return True

    return False

