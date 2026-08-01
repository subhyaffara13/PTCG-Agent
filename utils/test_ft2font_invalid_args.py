
def test_ft2font_invalid_args(tmp_path):
    # filename argument.
    with pytest.raises(TypeError, match='to a font file or a binary-mode file object'):
        ft2font.FT2Font(None)
    with pytest.raises(TypeError, match='to a font file or a binary-mode file object'):
        ft2font.FT2Font(object())  # Not bytes or string, and has no read() method.
    file = tmp_path / 'invalid-font.ttf'
    file.write_text('This is not a valid font file.')
    with (pytest.raises(TypeError, match='to a font file or a binary-mode file object'),
          file.open('rt') as fd):
        ft2font.FT2Font(fd)
    with (pytest.raises(TypeError, match='to a font file or a binary-mode file object'),
          file.open('wt') as fd):
        ft2font.FT2Font(fd)
    with (pytest.raises(TypeError, match='to a font file or a binary-mode file object'),
          file.open('wb') as fd):
        ft2font.FT2Font(fd)

    file = fm.findfont('DejaVu Sans')

    # hinting_factor argument.
    with pytest.raises(TypeError, match='incompatible constructor arguments'):
        ft2font.FT2Font(file, 1.3)
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match='text.hinting_factor rcParam was deprecated .+ 3.11'):
        mpl.rcParams['text.hinting_factor'] = 8
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match='The hinting_factor parameter was deprecated'):
        ft2font.FT2Font(file, 0)

    with pytest.raises(TypeError, match='incompatible constructor arguments'):
        # failing to be a list will fail before the 0
        ft2font.FT2Font(file, _fallback_list=(0,))
    with pytest.raises(TypeError, match='incompatible constructor arguments'):
        ft2font.FT2Font(file, _fallback_list=[0])

    # kerning_factor argument.
    with pytest.raises(TypeError, match='incompatible constructor arguments'):
        ft2font.FT2Font(file, _kerning_factor=1.3)
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match='text.kerning_factor rcParam was deprecated .+ 3.11'):
        mpl.rcParams['text.kerning_factor'] = 0
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match='_kerning_factor parameter was deprecated .+ 3.11'):
        ft2font.FT2Font(file, _kerning_factor=123)

