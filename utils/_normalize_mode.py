
def _normalize_mode(im: Image.Image) -> Image.Image:
    """
    Takes an image (or frame), returns an image in a mode that is appropriate
    for saving in a Gif.

    It may return the original image, or it may return an image converted to
    palette or 'L' mode.

    :param im: Image object
    :returns: Image object
    """
    if im.mode in RAWMODE:
        im.load()
        return im
    if Image.getmodebase(im.mode) == "RGB":
        im = im.convert("P", palette=Image.Palette.ADAPTIVE)
        assert im.palette is not None
        if im.palette.mode == "RGBA":
            for rgba in im.palette.colors:
                if rgba[3] == 0:
                    im.info["transparency"] = im.palette.colors[rgba]
                    break
        return im
    return im.convert("L")

