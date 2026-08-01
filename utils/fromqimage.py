
def fromqimage(im: ImageQt.QImage) -> ImageFile.ImageFile:
    """Creates an image instance from a QImage image"""
    from . import ImageQt

    if not ImageQt.qt_is_installed:
        msg = "Qt bindings are not installed"
        raise ImportError(msg)
    return ImageQt.fromqimage(im)


def fromqimage(im: QImage | QPixmap) -> ImageFile.ImageFile:
    """
    :param im: QImage or PIL ImageQt object
    """
    buffer = QBuffer()
    qt_openmode: object
    if qt_version == "6":
        try:
            qt_openmode = getattr(QIODevice, "OpenModeFlag")
        except AttributeError:
            qt_openmode = getattr(QIODevice, "OpenMode")
    else:
        qt_openmode = QIODevice
    buffer.open(getattr(qt_openmode, "ReadWrite"))
    # preserve alpha channel with png
    # otherwise ppm is more friendly with Image.open
    if im.hasAlphaChannel():
        im.save(buffer, "png")
    else:
        im.save(buffer, "ppm")

    b = BytesIO()
    b.write(buffer.data())
    buffer.close()
    b.seek(0)

    return Image.open(b)

