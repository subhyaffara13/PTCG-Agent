from typing import Any

def _toqclass_helper(im: Image.Image | str | QByteArray) -> dict[str, Any]:
    data = None
    colortable = None
    exclusive_fp = False

    # handle filename, if given instead of image name
    if hasattr(im, "toUtf8"):
        # FIXME - is this really the best way to do this?
        im = str(im.toUtf8(), "utf-8")
    if is_path(im):
        im = Image.open(im)
        exclusive_fp = True
    assert isinstance(im, Image.Image)

    qt_format = getattr(QImage, "Format") if qt_version == "6" else QImage
    if im.mode == "1":
        format = getattr(qt_format, "Format_Mono")
    elif im.mode == "L":
        format = getattr(qt_format, "Format_Indexed8")
        colortable = [rgb(i, i, i) for i in range(256)]
    elif im.mode == "P":
        format = getattr(qt_format, "Format_Indexed8")
        palette = im.getpalette()
        assert palette is not None
        colortable = [rgb(*palette[i : i + 3]) for i in range(0, len(palette), 3)]
    elif im.mode == "RGB":
        # Populate the 4th channel with 255
        im = im.convert("RGBA")

        data = im.tobytes("raw", "BGRA")
        format = getattr(qt_format, "Format_RGB32")
    elif im.mode == "RGBA":
        data = im.tobytes("raw", "BGRA")
        format = getattr(qt_format, "Format_ARGB32")
    elif im.mode == "I;16":
        im = im.point(lambda i: i * 256)

        format = getattr(qt_format, "Format_Grayscale16")
    else:
        if exclusive_fp:
            im.close()
        msg = f"unsupported image mode {repr(im.mode)}"
        raise ValueError(msg)

    size = im.size
    __data = data or align8to32(im.tobytes(), size[0], im.mode)
    if exclusive_fp:
        im.close()
    return {"data": __data, "size": size, "format": format, "colortable": colortable}

