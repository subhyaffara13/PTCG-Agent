
def _get_background(
    im: Image.Image,
    info_background: int | tuple[int, int, int] | tuple[int, int, int, int] | None,
) -> int:
    background = 0
    if info_background:
        if isinstance(info_background, tuple):
            # WebPImagePlugin stores an RGBA value in info["background"]
            # So it must be converted to the same format as GifImagePlugin's
            # info["background"] - a global color table index
            assert im.palette is not None
            try:
                background = im.palette.getcolor(info_background, im)
            except ValueError as e:
                if str(e) not in (
                    # If all 256 colors are in use,
                    # then there is no need for the background color
                    "cannot allocate more than 256 colors",
                    # Ignore non-opaque WebP background
                    "cannot add non-opaque RGBA color to RGB palette",
                ):
                    raise
        else:
            background = info_background
    return background

