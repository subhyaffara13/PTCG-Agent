
def _maketile(
    file: IO[bytes], mode: str, bbox: tuple[int, int, int, int], channels: int
) -> list[ImageFile._Tile]:
    tiles = []
    read = file.read

    compression = i16(read(2))

    xsize = bbox[2] - bbox[0]
    ysize = bbox[3] - bbox[1]

    offset = file.tell()

    if compression == 0:
        #
        # raw compression
        for channel in range(channels):
            layer = mode[channel]
            if mode == "CMYK":
                layer += ";I"
            tiles.append(ImageFile._Tile("raw", bbox, offset, layer))
            offset = offset + xsize * ysize

    elif compression == 1:
        #
        # packbits compression
        i = 0
        bytecount = read(channels * ysize * 2)
        offset = file.tell()
        for channel in range(channels):
            layer = mode[channel]
            if mode == "CMYK":
                layer += ";I"
            tiles.append(ImageFile._Tile("packbits", bbox, offset, layer))
            for y in range(ysize):
                offset = offset + i16(bytecount, i)
                i += 2

    file.seek(offset)

    if offset & 1:
        read(1)  # padding

    return tiles

