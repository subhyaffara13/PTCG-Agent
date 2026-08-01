
def _parse_jp2_header(
    fp: IO[bytes],
) -> tuple[
    tuple[int, int],
    str,
    str | None,
    tuple[float, float] | None,
    ImagePalette.ImagePalette | None,
]:
    """Parse the JP2 header box to extract size, component count,
    color space information, and optionally DPI information,
    returning a (size, mode, mimetype, dpi) tuple."""

    # Find the JP2 header box
    reader = BoxReader(fp)
    header = None
    mimetype = None
    while reader.has_next_box():
        tbox = reader.next_box_type()

        if tbox == b"jp2h":
            header = reader.read_boxes()
            break
        elif tbox == b"ftyp":
            if reader.read_fields(">4s")[0] == b"jpx ":
                mimetype = "image/jpx"
    assert header is not None

    size = None
    mode = None
    bpc = None
    nc = None
    dpi = None  # 2-tuple of DPI info, or None
    palette = None
    colr = None

    while header.has_next_box():
        tbox = header.next_box_type()

        if tbox == b"ihdr":
            height, width, nc, bpc = header.read_fields(">IIHB")
            assert isinstance(height, int)
            assert isinstance(width, int)
            assert isinstance(bpc, int)
            size = (width, height)
            if nc == 1 and (bpc & 0x7F) > 8:
                mode = "I;16"
            elif nc == 1:
                mode = "L"
            elif nc == 2:
                mode = "LA"
            elif nc == 3:
                mode = "RGB"
            elif nc == 4:
                mode = "RGBA"
        elif tbox == b"colr":
            meth, _, _, enumcs = header.read_fields(">BBBI")
            if meth == 1:
                if enumcs in (0, 15):
                    colr = "1"
                elif enumcs == 12:
                    colr = "CMYK"
                    if nc == 4:
                        mode = "CMYK"
                elif enumcs == 17:
                    colr = "L"
        elif tbox == b"pclr" and mode in ("L", "LA") and colr not in ("1", "L"):
            ne, npc = header.read_fields(">HB")
            assert isinstance(ne, int)
            assert isinstance(npc, int)
            max_bitdepth = 0
            for bitdepth in header.read_fields(">" + ("B" * npc)):
                assert isinstance(bitdepth, int)
                if bitdepth > max_bitdepth:
                    max_bitdepth = bitdepth
            if max_bitdepth <= 8:
                if npc == 4:
                    palette_mode = "CMYK" if colr == "CMYK" else "RGBA"
                else:
                    palette_mode = "RGB"
                palette = ImagePalette.ImagePalette(palette_mode)
                for i in range(ne):
                    color: list[int] = []
                    for value in header.read_fields(">" + ("B" * npc)):
                        assert isinstance(value, int)
                        color.append(value)
                    palette.getcolor(tuple(color))
                mode = "P" if mode == "L" else "PA"
        elif tbox == b"res ":
            res = header.read_boxes()
            while res.has_next_box():
                tres = res.next_box_type()
                if tres == b"resc":
                    vrcn, vrcd, hrcn, hrcd, vrce, hrce = res.read_fields(">HHHHBB")
                    assert isinstance(vrcn, int)
                    assert isinstance(vrcd, int)
                    assert isinstance(hrcn, int)
                    assert isinstance(hrcd, int)
                    assert isinstance(vrce, int)
                    assert isinstance(hrce, int)
                    hres = _res_to_dpi(hrcn, hrcd, hrce)
                    vres = _res_to_dpi(vrcn, vrcd, vrce)
                    if hres is not None and vres is not None:
                        dpi = (hres, vres)
                    break

    if size is None or mode is None:
        msg = "Malformed JP2 header"
        raise SyntaxError(msg)

    return size, mode, mimetype, dpi, palette

