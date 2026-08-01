
def grayscale(image: Image.Image) -> Image.Image:
    """
    Convert the image to grayscale.

    :param image: The image to convert.
    :return: An image.
    """
    return image.convert("L")

