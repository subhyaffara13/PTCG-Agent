
def test_ft2font_language_invalid(input):
    file = fm.findfont('DejaVu Sans')
    font = ft2font.FT2Font(file)
    with pytest.raises(TypeError):
        font.set_text('foo', language=input)

