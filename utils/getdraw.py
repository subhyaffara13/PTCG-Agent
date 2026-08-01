
def getdraw(im: Image.Image | None = None) -> tuple[ImageDraw2.Draw | None, ModuleType]:
    """
    :param im: The image to draw in.
    :returns: A (drawing context, drawing resource factory) tuple.
    """
    from . import ImageDraw2

    draw = ImageDraw2.Draw(im) if im is not None else None
    return draw, ImageDraw2

