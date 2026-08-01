
def test_DDM_getitem():
    dm = DDM([
        [ZZ(1), ZZ(2), ZZ(3)],
        [ZZ(4), ZZ(5), ZZ(6)],
        [ZZ(7), ZZ(8), ZZ(9)]], (3, 3), ZZ)

    assert dm.getitem(1, 1) == ZZ(5)
    assert dm.getitem(1, -2) == ZZ(5)
    assert dm.getitem(-1, -3) == ZZ(7)

    raises(IndexError, lambda: dm.getitem(3, 3))

