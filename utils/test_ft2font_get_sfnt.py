
def test_ft2font_get_sfnt(font_name, expected):
    file = fm.findfont(font_name)
    font = ft2font.FT2Font(file)
    sfnt = font.get_sfnt()
    for name, value in expected.items():
        # Macintosh, Unicode 1.0, English, name.
        assert sfnt.pop((1, 0, 0, name)) == value.encode('ascii')
        # Microsoft, Unicode, English United States, name.
        assert sfnt.pop((3, 1, 1033, name)) == value.encode('utf-16be')
    assert sfnt == {}

