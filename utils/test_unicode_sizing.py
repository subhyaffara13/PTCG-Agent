
def test_unicode_sizing():
    tp = mpl.textpath.TextToPath()
    scale1 = tp.get_glyphs_tex(mpl.font_manager.FontProperties(), "W")[0][0][3]
    scale2 = tp.get_glyphs_tex(mpl.font_manager.FontProperties(), r"\textwon")[0][0][3]
    assert scale1 == scale2

