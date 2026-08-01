
def test_gf_TC():
    assert gf_TC([], ZZ) == 0
    assert gf_TC([1], ZZ) == 1
    assert gf_TC([1, 2], ZZ) == 2

