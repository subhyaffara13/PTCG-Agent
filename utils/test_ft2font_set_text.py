
def test_ft2font_set_text():
    file = fm.findfont('DejaVu Sans')
    font = ft2font.FT2Font(file)
    font.set_size(12, 72)
    xys = font.set_text('')
    np.testing.assert_array_equal(xys, np.empty((0, 2)))
    assert font.get_width_height() == (0, 0)
    assert font.get_num_glyphs() == 0
    assert font.get_descent() == 0
    assert font.get_bitmap_offset() == (0, 0)
    # This string uses all the kerning pairs defined for test_ft2font_get_kerning.
    xys = font.set_text('AADAT.XC-J')
    np.testing.assert_array_equal(
        xys,
        [(0, 0), (533, 0), (1045, 0), (1608, 0), (2060, 0), (2417, 0), (2609, 0),
         (3065, 0), (3577, 0), (3940, 0)])
    assert font.get_width_height() == (4196, 768)
    assert font.get_num_glyphs() == 10
    assert font.get_descent() == 192
    assert font.get_bitmap_offset() == (6, 0)

