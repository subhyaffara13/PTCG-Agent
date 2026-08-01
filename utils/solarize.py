
def solarize(image: Image.Image, threshold: int = 128) -> Image.Image:
    """
    Invert all pixel values above a threshold.

    :param image: The image to solarize.
    :param threshold: All pixels above this grayscale level are inverted.
    :return: An image.
    """
    lut = []
    for i in range(256):
        if i < threshold:
            lut.append(i)
        else:
            lut.append(255 - i)
    return _lut(image, lut)

