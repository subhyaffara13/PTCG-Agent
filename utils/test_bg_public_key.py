
def test_bg_public_key():
    assert 5293 == bg_public_key(67, 79)
    assert 713 == bg_public_key(23, 31)
    raises(ValueError, lambda: bg_private_key(13, 17))

