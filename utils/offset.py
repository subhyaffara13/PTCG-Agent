
def offset(image: Image.Image, xoffset: int, yoffset: int | None = None) -> Image.Image:
    """Returns a copy of the image where data has been offset by the given
    distances. Data wraps around the edges. If ``yoffset`` is omitted, it
    is assumed to be equal to ``xoffset``.

    :param image: Input image.
    :param xoffset: The horizontal distance.
    :param yoffset: The vertical distance.  If omitted, both
        distances are set to the same value.
    :rtype: :py:class:`~PIL.Image.Image`
    """

    if yoffset is None:
        yoffset = xoffset
    image.load()
    return image._new(image.im.offset(xoffset, yoffset))


def offset(_offset):
    return _offset()


def offset():
    return CDay()


def Offset(x: float = 0, y: float = 0) -> Transform:
    """Return the identity transformation offset by x, y.

    :Example:
            >>> Offset(2, 3)
            <Transform [1 0 0 1 2 3]>
            >>>
    """
    return Transform(1, 0, 0, 1, x, y)

