
def posterize(image: Image.Image, bits: int) -> Image.Image:
    """
    Reduce the number of bits for each color channel.

    :param image: The image to posterize.
    :param bits: The number of bits to keep for each channel (1-8).
    :return: An image.
    """
    mask = ~(2 ** (8 - bits) - 1)
    lut = [i & mask for i in range(256)]
    return _lut(image, lut)

