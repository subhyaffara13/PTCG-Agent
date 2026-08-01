
def test_DDM_det():
    # 0x0 case
    A = DDM([], (0, 0), ZZ)
    assert A.det() == ZZ(1)

    # 1x1 case
    A = DDM([[ZZ(2)]], (1, 1), ZZ)
    assert A.det() == ZZ(2)

    # 2x2 case
    A = DDM([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    assert A.det() == ZZ(-2)

    # 3x3 with swap
    A = DDM([[ZZ(1), ZZ(2), ZZ(3)], [ZZ(1), ZZ(2), ZZ(4)], [ZZ(1), ZZ(2), ZZ(5)]], (3, 3), ZZ)
    assert A.det() == ZZ(0)

    # 2x2 QQ case
    A = DDM([[QQ(1, 2), QQ(1, 2)], [QQ(1, 3), QQ(1, 4)]], (2, 2), QQ)
    assert A.det() == QQ(-1, 24)

    # Nonsquare error
    A = DDM([[ZZ(1)], [ZZ(2)]], (2, 1), ZZ)
    raises(DMShapeError, lambda: A.det())

    # Nonsquare error with empty matrix
    A = DDM([], (0, 1), ZZ)
    raises(DMShapeError, lambda: A.det())

