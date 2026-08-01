
def test_ft2font_features():
    # Smoke test that these are accepted as intended.
    file = fm.findfont('DejaVu Sans')
    font = ft2font.FT2Font(file)
    font.set_text('foo', features=None)  # unset
    font.set_text('foo', features=['calt', 'dlig'])  # list
    font.set_text('foo', features=('calt', 'dlig'))  # tuple
    with pytest.raises(TypeError):
        font.set_text('foo', features=123)
    with pytest.raises(TypeError):
        font.set_text('foo', features=[123, 456])

