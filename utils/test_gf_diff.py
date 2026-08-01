
def test_gf_diff():
    assert gf_diff([], 11, ZZ) == []
    assert gf_diff([7], 11, ZZ) == []

    assert gf_diff([7, 3], 11, ZZ) == [7]
    assert gf_diff([7, 3, 1], 11, ZZ) == [3, 3]

    assert gf_diff([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 11, ZZ) == []

