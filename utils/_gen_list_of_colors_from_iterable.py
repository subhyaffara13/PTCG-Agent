
def _gen_list_of_colors_from_iterable(color: Collection[Color]) -> Iterator[Color]:
    """
    Yield colors from string of several letters or from collection of colors.
    """
    for x in color:
        if _is_single_color(x):
            yield x
        else:
            raise ValueError(f"Invalid color {x}")

