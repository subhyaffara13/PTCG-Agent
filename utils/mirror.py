
def mirror(image: Image.Image) -> Image.Image:
    """
    Flip image horizontally (left to right).

    :param image: The image to mirror.
    :return: An image.
    """
    return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

