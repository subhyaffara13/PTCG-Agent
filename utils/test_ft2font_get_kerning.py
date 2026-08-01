
def test_ft2font_get_kerning(left, right, unscaled, unfitted, default):
    file = fm.findfont('DejaVu Sans')
    # With unscaled, these settings should produce exact values found in FontForge.
    font = ft2font.FT2Font(file)
    font.set_size(100, 100)
    assert font.get_kerning(font.get_char_index(ord(left)),
                            font.get_char_index(ord(right)),
                            ft2font.Kerning.UNSCALED) == unscaled
    assert font.get_kerning(font.get_char_index(ord(left)),
                            font.get_char_index(ord(right)),
                            ft2font.Kerning.UNFITTED) == unfitted
    assert font.get_kerning(font.get_char_index(ord(left)),
                            font.get_char_index(ord(right)),
                            ft2font.Kerning.DEFAULT) == default
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match='Use Kerning.UNSCALED instead'):
        k = ft2font.KERNING_UNSCALED
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match='Use Kerning enum values instead'):
        assert font.get_kerning(font.get_char_index(ord(left)),
                                font.get_char_index(ord(right)),
                                int(k)) == unscaled
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match='Use Kerning.UNFITTED instead'):
        k = ft2font.KERNING_UNFITTED
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match='Use Kerning enum values instead'):
        assert font.get_kerning(font.get_char_index(ord(left)),
                                font.get_char_index(ord(right)),
                                int(k)) == unfitted
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match='Use Kerning.DEFAULT instead'):
        k = ft2font.KERNING_DEFAULT
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match='Use Kerning enum values instead'):
        assert font.get_kerning(font.get_char_index(ord(left)),
                                font.get_char_index(ord(right)),
                                int(k)) == default

