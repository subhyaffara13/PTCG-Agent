
def getheader(
    im: Image.Image, palette: _Palette | None = None, info: dict[str, Any] | None = None
) -> tuple[list[bytes], list[int] | None]:
    """
    Legacy Method to get Gif data from image.

    Warning:: May modify image data.

    :param im: Image object
    :param palette: bytes object containing the source palette, or ....
    :param info: encoderinfo
    :returns: tuple of(list of header items, optimized palette)

    """
    if info is None:
        info = {}

    used_palette_colors = _get_optimize(im, info)

    if "background" not in info and "background" in im.info:
        info["background"] = im.info["background"]

    im_mod = _normalize_palette(im, palette, info)
    im.palette = im_mod.palette
    im.im = im_mod.im
    header = _get_global_header(im, info)

    return header, used_palette_colors

