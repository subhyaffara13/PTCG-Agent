
def test_ft2font_drawing():
    expected_str = (
        '          ',
        '11    11  ',
        '11    11  ',
        '1 1  1 1  ',
        '1 1  1 1  ',
        '1 1  1 1  ',
        '1  11  1  ',
        '1  11  1  ',
        '1      1  ',
        '1      1  ',
        '          ',
    )
    expected = np.array([
        [int(c) for c in line.replace(' ', '0')] for line in expected_str
    ])
    expected *= 255
    file = fm.findfont('DejaVu Sans')
    font = ft2font.FT2Font(file)
    font.set_size(12, 72)
    font.set_text('M')
    font.draw_glyphs_to_bitmap(antialiased=False)
    image = font.get_image()
    np.testing.assert_array_equal(image, expected)
    font = ft2font.FT2Font(file)
    font.set_size(12, 72)
    glyph = font.load_char(ord('M'))
    image = np.zeros(expected.shape, np.uint8)
    font.draw_glyph_to_bitmap(image, -1, 1, glyph, antialiased=False)
    np.testing.assert_array_equal(image, expected)

