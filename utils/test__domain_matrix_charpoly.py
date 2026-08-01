
def test_DomainMatrix_charpoly():
    A = DomainMatrix([], (0, 0), ZZ)
    p = [ZZ(1)]
    assert A.charpoly() == p
    assert A.to_sparse().charpoly() == p

    A = DomainMatrix([[1]], (1, 1), ZZ)
    p = [ZZ(1), ZZ(-1)]
    assert A.charpoly() == p
    assert A.to_sparse().charpoly() == p

    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    p = [ZZ(1), ZZ(-5), ZZ(-2)]
    assert A.charpoly() == p
    assert A.to_sparse().charpoly() == p

    A = DomainMatrix([[ZZ(1), ZZ(2), ZZ(3)], [ZZ(4), ZZ(5), ZZ(6)], [ZZ(7), ZZ(8), ZZ(9)]], (3, 3), ZZ)
    p = [ZZ(1), ZZ(-15), ZZ(-18), ZZ(0)]
    assert A.charpoly() == p
    assert A.to_sparse().charpoly() == p

    A = DomainMatrix([[ZZ(0), ZZ(1), ZZ(0)],
                      [ZZ(1), ZZ(0), ZZ(1)],
                      [ZZ(0), ZZ(1), ZZ(0)]], (3, 3), ZZ)
    p = [ZZ(1), ZZ(0), ZZ(-2), ZZ(0)]
    assert A.charpoly() == p
    assert A.to_sparse().charpoly() == p

    A = DM([[17, 0, 30,  0,  0,  0, 0,  0, 0, 0],
            [ 0, 0,  0,  0,  0,  0, 0,  0, 0, 0],
            [69, 0,  0,  0,  0, 86, 0,  0, 0, 0],
            [23, 0,  0,  0,  0,  0, 0,  0, 0, 0],
            [ 0, 0,  0,  0,  0,  0, 0,  0, 0, 0],
            [ 0, 0,  0, 13,  0,  0, 0,  0, 0, 0],
            [ 0, 0,  0,  0,  0,  0, 0, 32, 0, 0],
            [ 0, 0,  0,  0, 37, 67, 0,  0, 0, 0],
            [ 0, 0,  0,  0,  0,  0, 0,  0, 0, 0],
            [ 0, 0,  0,  0,  0,  0, 0,  0, 0, 0]], ZZ)
    p = ZZ.map([1, -17, -2070, 0, -771420, 0, 0, 0, 0, 0, 0])
    assert A.charpoly() == p
    assert A.to_sparse().charpoly() == p

    Ans = DomainMatrix([[QQ(1), QQ(2)]], (1, 2), QQ)
    raises(DMNonSquareMatrixError, lambda: Ans.charpoly())

