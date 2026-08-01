
def test_dup_sub_ground():
    f = ZZ.map([1, 2, 3, 4])
    g = ZZ.map([1, 2, 3, 0])

    assert dup_sub_ground(f, ZZ(4), ZZ) == g

