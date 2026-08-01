
def test_gm_public_key():
    assert 323 == gm_public_key(17, 19)[1]
    assert 15  == gm_public_key(3, 5)[1]
    raises(ValueError, lambda: gm_public_key(15, 19))

