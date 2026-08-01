
def test_gf_from_to_int_poly():
    assert gf_from_int_poly([1, 0, 7, 2, 20], 5) == [1, 0, 2, 2, 0]
    assert gf_to_int_poly([1, 0, 4, 2, 3], 5) == [1, 0, -1, 2, -2]

    assert gf_to_int_poly([10], 11, symmetric=True) == [-1]
    assert gf_to_int_poly([10], 11, symmetric=False) == [10]

