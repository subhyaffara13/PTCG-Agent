
def fromqpixmap(im: ImageQt.QPixmap) -> ImageFile.ImageFile:
    """Creates an image instance from a QPixmap image"""
    from . import ImageQt

    if not ImageQt.qt_is_installed:
        msg = "Qt bindings are not installed"
        raise ImportError(msg)
    return ImageQt.fromqpixmap(im)


def fromqpixmap(im: QPixmap) -> ImageFile.ImageFile:
    return fromqimage(im)

