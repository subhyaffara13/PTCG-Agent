
def _write_local_header(
    fp: IO[bytes], im: Image.Image, offset: tuple[int, int], flags: int
) -> None:
    try:
        transparency = im.encoderinfo["transparency"]
    except KeyError:
        transparency = None

    if "duration" in im.encoderinfo:
        duration = int(im.encoderinfo["duration"] / 10)
    else:
        duration = 0

    disposal = int(im.encoderinfo.get("disposal", 0))

    if transparency is not None or duration != 0 or disposal:
        packed_flag = 1 if transparency is not None else 0
        packed_flag |= disposal << 2

        fp.write(
            b"!"
            + o8(249)  # extension intro
            + o8(4)  # length
            + o8(packed_flag)  # packed fields
            + o16(duration)  # duration
            + o8(transparency or 0)  # transparency index
            + o8(0)
        )

    include_color_table = im.encoderinfo.get("include_color_table")
    if include_color_table:
        palette_bytes = _get_palette_bytes(im)
        color_table_size = _get_color_table_size(palette_bytes)
        if color_table_size:
            flags = flags | 128  # local color table flag
            flags = flags | color_table_size

    fp.write(
        b","
        + o16(offset[0])  # offset
        + o16(offset[1])
        + o16(im.size[0])  # size
        + o16(im.size[1])
        + o8(flags)  # flags
    )
    if include_color_table and color_table_size:
        fp.write(_get_header_palette(palette_bytes))
    fp.write(o8(8))  # bits

