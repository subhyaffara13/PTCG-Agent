
def test_DDM_setitem():
    dm = DDM.zeros((3, 3), ZZ)
    dm.setitem(0, 0, 1)
    dm.setitem(1, -2, 1)
    dm.setitem(-1, -1, 1)
    assert dm == DDM.eye(3, ZZ)

    raises(IndexError, lambda: dm.setitem(3, 3, 0))

