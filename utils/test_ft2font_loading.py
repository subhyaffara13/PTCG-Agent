
def test_ft2font_loading():
    file = fm.findfont('DejaVu Sans')
    font = ft2font.FT2Font(file)
    font.set_size(12, 72)
    for glyph in [font.load_char(ord('M')),
                  font.load_glyph(font.get_char_index(ord('M')))]:
        assert glyph is not None
        assert glyph.width == 576
        assert glyph.height == 576
        assert glyph.horiBearingX == 0
        assert glyph.horiBearingY == 576
        assert glyph.horiAdvance == 640
        assert glyph.linearHoriAdvance == 678528
        assert glyph.vertBearingX == -384
        assert glyph.vertBearingY == 64
        assert glyph.vertAdvance == 832
        assert glyph.bbox == (54, 0, 574, 576)
    assert font.get_num_glyphs() == 2  # Both count as loaded.
    # But neither has been placed anywhere.
    assert font.get_width_height() == (0, 0)
    assert font.get_descent() == 0
    assert font.get_bitmap_offset() == (0, 0)

