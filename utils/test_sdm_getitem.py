
def test_SDM_getitem():
    A = SDM({0:{1:ZZ(1)}}, (2, 2), ZZ)
    assert A.getitem(0, 0) == ZZ.zero
    assert A.getitem(0, 1) == ZZ.one
    assert A.getitem(1, 0) == ZZ.zero
    assert A.getitem(-2, -2) == ZZ.zero
    assert A.getitem(-2, -1) == ZZ.one
    assert A.getitem(-1, -2) == ZZ.zero
    raises(IndexError, lambda: A.getitem(2, 0))
    raises(IndexError, lambda: A.getitem(0, 2))

