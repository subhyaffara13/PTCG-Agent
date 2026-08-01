
def _get_colors_from_color(
    color: Color | Collection[Color],
) -> list[Color]:
    """Get colors from user input color."""
    if len(color) == 0:
        raise ValueError(f"Invalid color argument: {color}")

    if _is_single_color(color):
        color = cast(Color, color)
        return [color]

    color = cast(Collection[Color], color)
    return list(_gen_list_of_colors_from_iterable(color))

