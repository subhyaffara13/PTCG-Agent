
def test_DomainMatrix_inv():
    A = DomainMatrix([], (0, 0), QQ)
    assert A.inv() == A

    A = DomainMatrix([[QQ(1), QQ(2)], [QQ(3), QQ(4)]], (2, 2), QQ)
    Ainv = DomainMatrix([[QQ(-2), QQ(1)], [QQ(3, 2), QQ(-1, 2)]], (2, 2), QQ)
    assert A.inv() == Ainv

    Az = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    raises(DMNotAField, lambda: Az.inv())

    Ans = DomainMatrix([[QQ(1), QQ(2)]], (1, 2), QQ)
    raises(DMNonSquareMatrixError, lambda: Ans.inv())

    Aninv = DomainMatrix([[QQ(1), QQ(2)], [QQ(3), QQ(6)]], (2, 2), QQ)
    raises(DMNonInvertibleMatrixError, lambda: Aninv.inv())

    Z3 = FF(3)
    assert DM([[1, 2], [3, 4]], Z3).inv() == DM([[1, 1], [0, 1]], Z3)

    Z6 = FF(6)
    raises(DMNotAField, lambda: DM([[1, 2], [3, 4]], Z6).inv())

