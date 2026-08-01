
def test_SDM_setitem():
    A = SDM({0:{1:ZZ(1)}}, (2, 2), ZZ)
    A.setitem(0, 0, ZZ(1))
    assert A == SDM({0:{0:ZZ(1), 1:ZZ(1)}}, (2, 2), ZZ)
    A.setitem(1, 0, ZZ(1))
    assert A == SDM({0:{0:ZZ(1), 1:ZZ(1)}, 1:{0:ZZ(1)}}, (2, 2), ZZ)
    A.setitem(1, 0, ZZ(0))
    assert A == SDM({0:{0:ZZ(1), 1:ZZ(1)}}, (2, 2), ZZ)
    # Repeat the above test so that this time the row is empty
    A.setitem(1, 0, ZZ(0))
    assert A == SDM({0:{0:ZZ(1), 1:ZZ(1)}}, (2, 2), ZZ)
    A.setitem(0, 0, ZZ(0))
    assert A == SDM({0:{1:ZZ(1)}}, (2, 2), ZZ)
    # This time the row is there but column is empty
    A.setitem(0, 0, ZZ(0))
    assert A == SDM({0:{1:ZZ(1)}}, (2, 2), ZZ)
    raises(IndexError, lambda: A.setitem(2, 0, ZZ(1)))
    raises(IndexError, lambda: A.setitem(0, 2, ZZ(1)))

