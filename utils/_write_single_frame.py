
def _write_single_frame(
    im: Image.Image,
    fp: IO[bytes],
    palette: _Palette | None,
) -> None:
    im_out = _normalize_mode(im)
    for k, v in im_out.info.items():
        if isinstance(k, str):
            im.encoderinfo.setdefault(k, v)
    im_out = _normalize_palette(im_out, palette, im.encoderinfo)

    for s in _get_global_header(im_out, im.encoderinfo):
        fp.write(s)

    # local image header
    flags = 0
    if get_interlace(im):
        flags = flags | 64
    _write_local_header(fp, im, (0, 0), flags)

    im_out.encoderconfig = (8, get_interlace(im))
    ImageFile._save(
        im_out, fp, [ImageFile._Tile("gif", (0, 0) + im.size, 0, RAWMODE[im_out.mode])]
    )

    fp.write(b"\0")  # end of image data

