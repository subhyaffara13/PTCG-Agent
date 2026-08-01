
def _color(color: str | int | tuple[int, ...], mode: str) -> int | tuple[int, ...]:
    if isinstance(color, str):
        from . import ImageColor

        color = ImageColor.getcolor(color, mode)
    return color

