
def blend(im1: Image, im2: Image, alpha: float) -> Image:
    """
    Creates a new image by interpolating between two input images, using
    a constant alpha::

        out = image1 * (1.0 - alpha) + image2 * alpha

    :param im1: The first image.
    :param im2: The second image.  Must have the same mode and size as
       the first image.
    :param alpha: The interpolation alpha factor.  If alpha is 0.0, a
       copy of the first image is returned. If alpha is 1.0, a copy of
       the second image is returned. There are no restrictions on the
       alpha value. If necessary, the result is clipped to fit into
       the allowed output range.
    :returns: An :py:class:`~PIL.Image.Image` object.
    """

    im1.load()
    im2.load()
    return im1._new(core.blend(im1.im, im2.im, alpha))


def blend(image1: Image.Image, image2: Image.Image, alpha: float) -> Image.Image:
    """Blend images using constant transparency weight. Alias for
    :py:func:`PIL.Image.blend`.

    :rtype: :py:class:`~PIL.Image.Image`
    """

    return Image.blend(image1, image2, alpha)

