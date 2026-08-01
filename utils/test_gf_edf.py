
def test_gf_edf():
    f = ZZ.map([1, 1, 0, 1, 2])
    g = ZZ.map([[1, 0, 1], [1, 1, 2]])

    assert gf_edf_zassenhaus(f, 2, 3, ZZ) == g
    assert gf_edf_shoup(f, 2, 3, ZZ) == g

