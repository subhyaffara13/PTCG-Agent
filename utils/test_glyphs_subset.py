
def test_glyphs_subset():
    fpath = str(_get_data_path("fonts/ttf/DejaVuSerif.ttf"))
    chars = "these should be subsetted! 1234567890"

    # non-subsetted FT2Font
    nosubfont = FT2Font(fpath)
    nosubfont.set_text(chars)
    nosubcmap = nosubfont.get_charmap()

    # subsetted FT2Font
    glyph_indices = {nosubcmap[ord(c)] for c in chars}
    with get_glyphs_subset(fm.FontPath(fpath, 0), glyph_indices) as subset:
        subfont = FT2Font(font_as_file(subset))
    subfont.set_text(chars)
    subcmap = subfont.get_charmap()

    # all unique chars must be available in subsetted font
    assert {*chars} == {chr(key) for key in subcmap}

    # subsetted font's charmap should have less entries
    assert len(subcmap) < len(nosubcmap)

    # since both objects are assigned same characters
    assert subfont.get_num_glyphs() == nosubfont.get_num_glyphs()

