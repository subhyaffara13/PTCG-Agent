
def test_ft2font_clear():
    file = fm.findfont('DejaVu Sans')
    font = ft2font.FT2Font(file)
    assert font.get_num_glyphs() == 0
    assert font.get_width_height() == (0, 0)
    assert font.get_bitmap_offset() == (0, 0)
    font.set_text('ABabCDcd')
    assert font.get_num_glyphs() == 8
    assert font.get_width_height() != (0, 0)
    assert font.get_bitmap_offset() != (0, 0)
    font.clear()
    assert font.get_num_glyphs() == 0
    assert font.get_width_height() == (0, 0)
    assert font.get_bitmap_offset() == (0, 0)

