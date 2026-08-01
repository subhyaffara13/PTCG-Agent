
def test_gf_int():
    assert gf_int(0, 5) == 0
    assert gf_int(1, 5) == 1
    assert gf_int(2, 5) == 2
    assert gf_int(3, 5) == -2
    assert gf_int(4, 5) == -1
    assert gf_int(5, 5) == 0

