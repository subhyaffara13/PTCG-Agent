
def _get_pdf_charprocs(font_path, glyph_indices):
    font = get_font(font_path)
    conv = 1000 / font.units_per_EM  # Conversion to PS units (1/1000's).
    procs = {}
    for glyph_index in glyph_indices:
        g = font.load_glyph(glyph_index, LoadFlags.NO_SCALE)
        d1 = [
            round(g.horiAdvance * conv), 0,
            # Round bbox corners *outwards*, so that they indeed bound the glyph.
            math.floor(g.bbox[0] * conv), math.floor(g.bbox[1] * conv),
            math.ceil(g.bbox[2] * conv), math.ceil(g.bbox[3] * conv),
        ]
        v, c = font.get_path()
        v = (v * 64 * conv).round()  # Back to TrueType's internal units (1/64's).
        procs[font.get_glyph_name(glyph_index)] = (
            " ".join(map(str, d1)).encode("ascii") + b" d1\n"
            + _path.convert_to_string(
                Path(v, c), None, None, False, None, 0,
                # no code for quad Beziers triggers auto-conversion to cubics.
                [b"m", b"l", b"", b"c", b"h"], True)
            + b"f")
    return procs

