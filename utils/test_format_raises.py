
def test_format_raises(styler, formatter, func):
    with pytest.raises(TypeError, match="expected str or callable"):
        getattr(styler, func)(formatter)

