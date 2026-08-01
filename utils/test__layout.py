
def test__layout():
    fonts, test_str = _gen_multi_font_text()
    # Add some glyphs that don't exist in either font to check the Last Resort fallback.
    missing_glyphs = '\n几个汉字'
    test_str += missing_glyphs

    ft = fm.get_font(
        fm.fontManager._find_fonts_by_props(fm.FontProperties(family=fonts))
    )
    for substr in test_str.split('\n'):
        for item in ft._layout(substr, ft2font.LoadFlags.DEFAULT):
            if item.char in missing_glyphs:
                assert Path(item.ft_object.fname).name == 'LastResortHE-Regular.ttf'
            elif ord(item.char) > 127:
                assert Path(item.ft_object.fname).name == 'DejaVuSans.ttf'
            else:
                assert Path(item.ft_object.fname).name == 'cmr10.ttf'

