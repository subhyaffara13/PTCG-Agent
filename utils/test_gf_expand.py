
def test_gf_expand():
    F = [([1, 1], 2), ([1, 2], 3)]

    assert gf_expand(F, 11, ZZ) == [1, 8, 3, 5, 6, 8]
    assert gf_expand((4, F), 11, ZZ) == [4, 10, 1, 9, 2, 10]

