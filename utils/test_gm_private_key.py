
def test_gm_private_key():
    raises(ValueError, lambda: gm_public_key(13, 15))
    raises(ValueError, lambda: gm_public_key(0, 0))
    raises(ValueError, lambda: gm_public_key(0, 5))
    assert 17, 19 == gm_public_key(17, 19)

