
def getimage(photo: PhotoImage) -> Image.Image:
    """Copies the contents of a PhotoImage to a PIL image memory."""
    im = Image.new("RGBA", (photo.width(), photo.height()))

    _pyimagingtkcall("PyImagingPhotoGet", photo, im.getim())

    return im

