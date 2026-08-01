
def test_get_numbered_constants():
    with raises(ValueError):
        get_numbered_constants(None)

