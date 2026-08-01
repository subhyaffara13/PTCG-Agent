
def _get_palette_bytes(im: Image.Image) -> bytes:
    """
    Gets the palette for inclusion in the gif header

    :param im: Image object
    :returns: Bytes, len<=768 suitable for inclusion in gif header
    """
    if not im.palette:
        return b""

    palette = bytes(im.palette.palette)
    if im.palette.mode == "RGBA":
        palette = b"".join(palette[i * 4 : i * 4 + 3] for i in range(len(palette) // 3))
    return palette

