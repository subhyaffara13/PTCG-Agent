
def test_DDM_inv():
    A = DDM([[QQ(1, 1), QQ(2, 1)], [QQ(3, 1), QQ(4, 1)]], (2, 2), QQ)
    Ainv = DDM([[QQ(-2, 1), QQ(1, 1)], [QQ(3, 2), QQ(-1, 2)]], (2, 2), QQ)
    assert A.inv() == Ainv

    A = DDM([[QQ(1), QQ(2)]], (1, 2), QQ)
    raises(DMShapeError, lambda: A.inv())

    A = DDM([[ZZ(2)]], (1, 1), ZZ)
    raises(DMDomainError, lambda: A.inv())

    A = DDM([], (0, 0), QQ)
    assert A.inv() == A

    A = DDM([[QQ(1), QQ(2)], [QQ(2), QQ(4)]], (2, 2), QQ)
    raises(DMNonInvertibleMatrixError, lambda: A.inv())


def test_ddm_inv():
    A = []
    Ainv = []
    ddm_iinv(Ainv, A, QQ)
    assert Ainv == A

    A = []
    Ainv = []
    raises(DMDomainError, lambda: ddm_iinv(Ainv, A, ZZ))

    A = [[QQ(1), QQ(2)]]
    Ainv = [[QQ(0), QQ(0)]]
    raises(DMNonSquareMatrixError, lambda: ddm_iinv(Ainv, A, QQ))

    A = [[QQ(1, 1), QQ(2, 1)], [QQ(3, 1), QQ(4, 1)]]
    Ainv = [[QQ(0), QQ(0)], [QQ(0), QQ(0)]]
    Ainv_expected = [[QQ(-2, 1), QQ(1, 1)], [QQ(3, 2), QQ(-1, 2)]]
    ddm_iinv(Ainv, A, QQ)
    assert Ainv == Ainv_expected

    A = [[QQ(1, 1), QQ(2, 1)], [QQ(2, 1), QQ(4, 1)]]
    Ainv = [[QQ(0), QQ(0)], [QQ(0), QQ(0)]]
    raises(DMNonInvertibleMatrixError, lambda: ddm_iinv(Ainv, A, QQ))


def test_ddm_inv(name, A, A_inv, den):
    A = A.to_field().to_ddm()
    if den != 0:
        A_inv = (A_inv.to_field() / den).to_ddm()
        assert A.inv() == A_inv
    else:
        raises(DMNonInvertibleMatrixError, lambda: A.inv())

