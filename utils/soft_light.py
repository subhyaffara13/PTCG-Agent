
def soft_light(image1: Image.Image, image2: Image.Image) -> Image.Image:
    """
    Superimposes two images on top of each other using the Soft Light algorithm

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_soft_light(image2.im))

