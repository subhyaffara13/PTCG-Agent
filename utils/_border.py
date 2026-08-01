
def _border(border: int | tuple[int, ...]) -> tuple[int, int, int, int]:
    if isinstance(border, tuple):
        if len(border) == 2:
            left, top = right, bottom = border
        elif len(border) == 4:
            left, top, right, bottom = border
        else:
            msg = "border must be an integer, or a tuple of two or four elements"
            raise ValueError(msg)
    else:
        left = top = right = bottom = border
    return left, top, right, bottom

