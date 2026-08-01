
def load_font(fontFile, options, checkChecksums=0, dontLoadGlyphNames=False, lazy=True):
    font = ttLib.TTFont(
        fontFile,
        checkChecksums=checkChecksums,
        recalcBBoxes=options.recalc_bounds,
        recalcTimestamp=options.recalc_timestamp,
        lazy=lazy,
        fontNumber=options.font_number,
    )

    # Hack:
    #
    # If we don't need glyph names, change 'post' class to not try to
    # load them.	It avoid lots of headache with broken fonts as well
    # as loading time.
    #
    # Ideally ttLib should provide a way to ask it to skip loading
    # glyph names.	But it currently doesn't provide such a thing.
    #
    if dontLoadGlyphNames:
        post = ttLib.getTableClass("post")
        saved = post.decode_format_2_0
        post.decode_format_2_0 = post.decode_format_3_0
        f = font["post"]
        if f.formatType == 2.0:
            f.formatType = 3.0
        post.decode_format_2_0 = saved

    return font

