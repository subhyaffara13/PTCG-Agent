
def _layerinfo(
    fp: IO[bytes], ct_bytes: int
) -> list[tuple[str, str, tuple[int, int, int, int], list[ImageFile._Tile]]]:
    # read layerinfo block
    layers = []

    def read(size: int) -> bytes:
        return ImageFile._safe_read(fp, size)

    ct = si16(read(2))

    # sanity check
    if ct_bytes < (abs(ct) * 20):
        msg = "Layer block too short for number of layers requested"
        raise SyntaxError(msg)

    for _ in range(abs(ct)):
        # bounding box
        y0 = si32(read(4))
        x0 = si32(read(4))
        y1 = si32(read(4))
        x1 = si32(read(4))

        # image info
        bands = []
        ct_types = i16(read(2))
        if ct_types > 4:
            fp.seek(ct_types * 6 + 12, io.SEEK_CUR)
            size = i32(read(4))
            fp.seek(size, io.SEEK_CUR)
            continue

        for _ in range(ct_types):
            channel_id = i16(read(2))

            if channel_id == 65535:
                b = "A"
            elif channel_id < 4:
                b = "RGBA"[channel_id]
            else:
                b = ""

            bands.append(b)
            read(4)  # size

        # figure out the image mode
        bands.sort()
        if bands == ["R"]:
            mode = "L"
        elif bands == ["B", "G", "R"]:
            mode = "RGB"
        elif bands == ["A", "B", "G", "R"]:
            mode = "RGBA"
        else:
            mode = ""  # unknown

        # skip over blend flags and extra information
        read(12)  # filler
        name = ""
        size = i32(read(4))  # length of the extra data field
        if size:
            data_end = fp.tell() + size

            length = i32(read(4))
            if length:
                fp.seek(length - 16, io.SEEK_CUR)

            length = i32(read(4))
            if length:
                fp.seek(length, io.SEEK_CUR)

            length = i8(read(1))
            if length:
                # Don't know the proper encoding,
                # Latin-1 should be a good guess
                name = read(length).decode("latin-1", "replace")

            fp.seek(data_end)
        layers.append((name, mode, (x0, y0, x1, y1)))

    # get tiles
    layerinfo = []
    for i, (name, mode, bbox) in enumerate(layers):
        tile = []
        for m in mode:
            t = _maketile(fp, m, bbox, 1)
            if t:
                tile.extend(t)
        layerinfo.append((name, mode, bbox, tile))

    return layerinfo

