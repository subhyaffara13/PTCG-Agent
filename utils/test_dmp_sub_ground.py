
def test_dmp_sub_ground():
    f = ZZ.map([[1], [2], [3], [4]])
    g = ZZ.map([[1], [2], [3], []])

    assert dmp_sub_ground(f, ZZ(4), 1, ZZ) == g

