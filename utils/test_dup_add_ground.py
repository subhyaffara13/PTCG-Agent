
def test_dup_add_ground():
    f = ZZ.map([1, 2, 3, 4])
    g = ZZ.map([1, 2, 3, 8])

    assert dup_add_ground(f, ZZ(4), ZZ) == g

