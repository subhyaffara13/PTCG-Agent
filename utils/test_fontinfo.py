
def test_fontinfo():
    fontpath = mpl.font_manager.findfont("DejaVu Sans")
    font = mpl.ft2font.FT2Font(fontpath)
    table = font.get_sfnt_table("head")
    assert table is not None
    assert table['version'] == (1, 0)

