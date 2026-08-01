
def test_XDM_setitem(DM):
    """Test setitem for DDM, etc."""

    A = DM([[0, 1, 2], [3, 4, 5]])

    A.setitem(0, 0, ZZ(6))
    assert A == DM([[6, 1, 2], [3, 4, 5]])

    A.setitem(0, 1, ZZ(7))
    assert A == DM([[6, 7, 2], [3, 4, 5]])

    A.setitem(0, 2, ZZ(8))
    assert A == DM([[6, 7, 8], [3, 4, 5]])

    A.setitem(0, -1, ZZ(9))
    assert A == DM([[6, 7, 9], [3, 4, 5]])

    A.setitem(0, -2, ZZ(10))
    assert A == DM([[6, 10, 9], [3, 4, 5]])

    A.setitem(0, -3, ZZ(11))
    assert A == DM([[11, 10, 9], [3, 4, 5]])

    raises(IndexError, lambda: A.setitem(0, 3, ZZ(12)))
    raises(IndexError, lambda: A.setitem(0, -4, ZZ(13)))

    A.setitem(1, 0, ZZ(14))
    assert A == DM([[11, 10, 9], [14, 4, 5]])

    A.setitem(1, 1, ZZ(15))
    assert A == DM([[11, 10, 9], [14, 15, 5]])

    A.setitem(-1, 1, ZZ(16))
    assert A == DM([[11, 10, 9], [14, 16, 5]])

    A.setitem(-2, 1, ZZ(17))
    assert A == DM([[11, 17, 9], [14, 16, 5]])

    raises(IndexError, lambda: A.setitem(2, 0, ZZ(18)))
    raises(IndexError, lambda: A.setitem(-3, 0, ZZ(19)))

    A.setitem(1, 2, ZZ(0))
    assert A == DM([[11, 17, 9], [14, 16, 0]])

    A.setitem(1, -2, ZZ(0))
    assert A == DM([[11, 17, 9], [14, 0, 0]])

    A.setitem(1, -3, ZZ(0))
    assert A == DM([[11, 17, 9], [0, 0, 0]])

    A.setitem(0, 0, ZZ(0))
    assert A == DM([[0, 17, 9], [0, 0, 0]])

    A.setitem(0, -1, ZZ(0))
    assert A == DM([[0, 17, 0], [0, 0, 0]])

    A.setitem(0, 0, ZZ(0))
    assert A == DM([[0, 17, 0], [0, 0, 0]])

    A.setitem(0, -2, ZZ(0))
    assert A == DM([[0, 0, 0], [0, 0, 0]])

    A.setitem(0, -3, ZZ(1))
    assert A == DM([[1, 0, 0], [0, 0, 0]])

