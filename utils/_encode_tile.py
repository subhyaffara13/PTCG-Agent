
def _encode_tile(
    im: Image.Image,
    fp: IO[bytes],
    tile: list[_Tile],
    bufsize: int,
    fh: int | None,
    exc: BaseException | None = None,
) -> None:
    for encoder_name, extents, offset, args in tile:
        if offset > 0:
            fp.seek(offset)
        encoder = Image._getencoder(im.mode, encoder_name, args, im.encoderconfig)
        try:
            encoder.setimage(im.im, extents)
            if encoder.pushes_fd:
                encoder.setfd(fp)
                errcode = encoder.encode_to_pyfd()[1]
            else:
                if exc:
                    # compress to Python file-compatible object
                    while True:
                        errcode, data = encoder.encode(bufsize)[1:]
                        fp.write(data)
                        if errcode:
                            break
                else:
                    # slight speedup: compress to real file object
                    assert fh is not None
                    errcode = encoder.encode_to_file(fh, bufsize)
            if errcode < 0:
                raise _get_oserror(errcode, encoder=True) from exc
        finally:
            encoder.cleanup()

