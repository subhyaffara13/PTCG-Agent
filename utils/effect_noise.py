
def effect_noise(size: tuple[int, int], sigma: float) -> Image:
    """
    Generate Gaussian noise centered around 128.

    :param size: The requested size in pixels, as a 2-tuple:
       (width, height).
    :param sigma: Standard deviation of noise.
    """
    return Image()._new(core.effect_noise(size, sigma))

