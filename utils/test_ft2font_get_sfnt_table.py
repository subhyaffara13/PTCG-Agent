
def test_ft2font_get_sfnt_table(font_name, header):
    file = fm.findfont(font_name)
    font = ft2font.FT2Font(file)
    assert font.get_sfnt_table(header) == _expected_sfnt_tables[font_name][header]

