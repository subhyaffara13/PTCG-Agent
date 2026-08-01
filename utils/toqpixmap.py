
def toqpixmap(im: Image.Image | str | QByteArray) -> QPixmap:
    qimage = toqimage(im)
    pixmap = getattr(QPixmap, "fromImage")(qimage)
    if qt_version == "6":
        pixmap.detach()
    return pixmap

