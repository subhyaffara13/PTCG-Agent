
def exif_transpose(image: Image.Image, *, in_place: Literal[True]) -> None: ...


def exif_transpose(
    image: Image.Image, *, in_place: Literal[False] = False
) -> Image.Image: ...


def exif_transpose(image: Image.Image, *, in_place: bool = False) -> Image.Image | None:
    """
    If an image has an EXIF Orientation tag, other than 1, transpose the image
    accordingly, and remove the orientation data.

    :param image: The image to transpose.
    :param in_place: Boolean. Keyword-only argument.
        If ``True``, the original image is modified in-place, and ``None`` is returned.
        If ``False`` (default), a new :py:class:`~PIL.Image.Image` object is returned
        with the transposition applied. If there is no transposition, a copy of the
        image will be returned.
    """
    image.load()
    image_exif = image.getexif()
    orientation = image_exif.get(ExifTags.Base.Orientation, 1)
    method = {
        2: Image.Transpose.FLIP_LEFT_RIGHT,
        3: Image.Transpose.ROTATE_180,
        4: Image.Transpose.FLIP_TOP_BOTTOM,
        5: Image.Transpose.TRANSPOSE,
        6: Image.Transpose.ROTATE_270,
        7: Image.Transpose.TRANSVERSE,
        8: Image.Transpose.ROTATE_90,
    }.get(orientation)
    if method is not None:
        if in_place:
            image.im = image.im.transpose(method)
            image._size = image.im.size
        else:
            transposed_image = image.transpose(method)
        exif_image = image if in_place else transposed_image

        exif = exif_image.getexif()
        if ExifTags.Base.Orientation in exif:
            del exif[ExifTags.Base.Orientation]
            if "exif" in exif_image.info:
                exif_image.info["exif"] = exif.tobytes()
            elif "Raw profile type exif" in exif_image.info:
                exif_image.info["Raw profile type exif"] = exif.tobytes().hex()
            for key in ("XML:com.adobe.xmp", "xmp"):
                if key in exif_image.info:
                    for pattern in (
                        r'tiff:Orientation="([0-9])"',
                        r"<tiff:Orientation>([0-9])</tiff:Orientation>",
                    ):
                        value = exif_image.info[key]
                        if isinstance(value, str):
                            value = re.sub(pattern, "", value)
                        elif isinstance(value, tuple):
                            value = tuple(
                                re.sub(pattern.encode(), b"", v) for v in value
                            )
                        else:
                            value = re.sub(pattern.encode(), b"", value)
                        exif_image.info[key] = value
        if not in_place:
            return transposed_image
    elif not in_place:
        return image.copy()
    return None

