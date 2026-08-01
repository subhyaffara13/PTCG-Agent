
def effect_mandelbrot(
    size: tuple[int, int], extent: tuple[float, float, float, float], quality: int
) -> Image:
    """
    Generate a Mandelbrot set covering the given extent.

    :param size: The requested size in pixels, as a 2-tuple:
       (width, height).
    :param extent: The extent to cover, as a 4-tuple:
       (x0, y0, x1, y1).
    :param quality: Quality.
    """
    return Image()._new(core.effect_mandelbrot(size, extent, quality))

