
def test_validate_cycler_bad_color_string():
    msg = "'foo' is neither a color sequence name nor can it be interpreted as a list"
    with pytest.raises(ValueError, match=msg):
        validate_cycler("cycler('color', 'foo')")

