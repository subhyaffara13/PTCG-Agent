
def _parse_codestream(fp: IO[bytes]) -> tuple[tuple[int, int], str]:
    """Parse the JPEG 2000 codestream to extract the size and component
    count from the SIZ marker segment, returning a PIL (size, mode) tuple."""

    hdr = fp.read(2)
    lsiz = _binary.i16be(hdr)
    if lsiz < 38:
        msg = "SIZ marker length must be at least 38"
        raise ValueError(msg)
    siz = hdr + fp.read(lsiz - 2)
    lsiz, rsiz, xsiz, ysiz, xosiz, yosiz, _, _, _, _, csiz = struct.unpack_from(
        ">HHIIIIIIIIH", siz
    )

    size = (xsiz - xosiz, ysiz - yosiz)
    if csiz == 1:
        ssiz = struct.unpack_from(">B", siz, 38)
        if (ssiz[0] & 0x7F) + 1 > 8:
            mode = "I;16"
        else:
            mode = "L"
    elif csiz == 2:
        mode = "LA"
    elif csiz == 3:
        mode = "RGB"
    elif csiz == 4:
        mode = "RGBA"
    else:
        msg = "unable to determine J2K image mode"
        raise SyntaxError(msg)

    return size, mode

