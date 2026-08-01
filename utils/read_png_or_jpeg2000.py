
def read_png_or_jpeg2000(
    fobj: IO[bytes], start_length: tuple[int, int], size: tuple[int, int, int]
) -> dict[str, Image.Image]:
    start, length = start_length
    fobj.seek(start)
    sig = fobj.read(12)

    im: Image.Image
    if sig.startswith(b"\x89PNG\x0d\x0a\x1a\x0a"):
        fobj.seek(start)
        im = PngImagePlugin.PngImageFile(fobj)
        Image._decompression_bomb_check(im.size)
        return {"RGBA": im}
    elif (
        sig.startswith((b"\xff\x4f\xff\x51", b"\x0d\x0a\x87\x0a"))
        or sig == b"\x00\x00\x00\x0cjP  \x0d\x0a\x87\x0a"
    ):
        if not enable_jpeg2k:
            msg = (
                "Unsupported icon subimage format (rebuild PIL "
                "with JPEG 2000 support to fix this)"
            )
            raise ValueError(msg)
        # j2k, jpc or j2c
        fobj.seek(start)
        jp2kstream = fobj.read(length)
        f = io.BytesIO(jp2kstream)
        im = Jpeg2KImagePlugin.Jpeg2KImageFile(f)
        Image._decompression_bomb_check(im.size)
        if im.mode != "RGBA":
            im = im.convert("RGBA")
        return {"RGBA": im}
    else:
        msg = "Unsupported icon subimage format"
        raise ValueError(msg)

