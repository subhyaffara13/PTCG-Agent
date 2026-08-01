
def read_mk(
    fobj: IO[bytes], start_length: tuple[int, int], size: tuple[int, int, int]
) -> dict[str, Image.Image]:
    # Alpha masks seem to be uncompressed
    start = start_length[0]
    fobj.seek(start)
    pixel_size = (size[0] * size[2], size[1] * size[2])
    sizesq = pixel_size[0] * pixel_size[1]
    band = Image.frombuffer("L", pixel_size, fobj.read(sizesq), "raw", "L", 0, 1)
    return {"A": band}

