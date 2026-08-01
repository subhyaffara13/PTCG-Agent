
def test_dmp_add_ground():
    f = ZZ.map([[1], [2], [3], [4]])
    g = ZZ.map([[1], [2], [3], [8]])

    assert dmp_add_ground(f, ZZ(4), 1, ZZ) == g

