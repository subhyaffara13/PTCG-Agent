
def test_ft2font_language():
    # This is just a smoke test.
    file = fm.findfont('DejaVu Sans')
    font = ft2font.FT2Font(file)
    font.set_text('foo')
    font.set_text('foo', language='en')
    font.set_text('foo', language=[('en', 1, 2)])

