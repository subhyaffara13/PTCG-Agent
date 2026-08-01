
def test_ft2font_set_size():
    file = fm.findfont('DejaVu Sans')
    font = ft2font.FT2Font(file)
    font.set_size(12, 72)
    font.set_text('ABabCDcd')
    orig = font.get_width_height()
    font.set_size(24, 72)
    font.set_text('ABabCDcd')
    assert font.get_width_height() == tuple(pytest.approx(2 * x, 1e-1) for x in orig)
    font.set_size(12, 144)
    font.set_text('ABabCDcd')
    assert font.get_width_height() == tuple(pytest.approx(2 * x, 1e-1) for x in orig)

