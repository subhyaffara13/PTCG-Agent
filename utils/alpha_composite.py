
def alpha_composite(im1: Image, im2: Image) -> Image:
    """
    Alpha composite im2 over im1.

    :param im1: The first image. Must have mode RGBA or LA.
    :param im2: The second image. Must have the same mode and size as the first image.
    :returns: An :py:class:`~PIL.Image.Image` object.
    """

    im1.load()
    im2.load()
    return im1._new(core.alpha_composite(im1.im, im2.im))

