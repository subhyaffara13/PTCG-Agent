
def test_gf_LC():
    assert gf_LC([], ZZ) == 0
    assert gf_LC([1], ZZ) == 1
    assert gf_LC([1, 2], ZZ) == 1

