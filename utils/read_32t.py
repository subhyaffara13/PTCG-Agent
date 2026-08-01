
def read_32t(
    fobj: IO[bytes], start_length: tuple[int, int], size: tuple[int, int, int]
) -> dict[str, Image.Image]:
    # The 128x128 icon seems to have an extra header for some reason.
    start, length = start_length
    fobj.seek(start)
    sig = fobj.read(4)
    if sig != b"\x00\x00\x00\x00":
        msg = "Unknown signature, expecting 0x00000000"
        raise SyntaxError(msg)
    return read_32(fobj, (start + 4, length - 4), size)

