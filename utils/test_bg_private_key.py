
def test_bg_private_key():
    raises(ValueError, lambda: bg_private_key(8, 16))
    raises(ValueError, lambda: bg_private_key(8, 8))
    raises(ValueError, lambda: bg_private_key(13, 17))
    assert 23, 31 == bg_private_key(23, 31)

