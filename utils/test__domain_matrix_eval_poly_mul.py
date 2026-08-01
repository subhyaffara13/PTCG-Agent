
def test_DomainMatrix_eval_poly_mul():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    b = DomainMatrix([[ZZ(1)], [ZZ(2)]], (2, 1), ZZ)
    p = [ZZ(1), ZZ(2), ZZ(3)]
    result = DomainMatrix([[ZZ(40)], [ZZ(87)]], (2, 1), ZZ)
    assert A.eval_poly_mul(p, b) == result == p[0]*A**2*b + p[1]*A*b + p[2]*b

    dM = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    dM1 = DomainMatrix([[ZZ(1)], [ZZ(2)]], (2, 1), ZZ)
    raises(DMNonSquareMatrixError, lambda: dM1.eval_poly_mul([ZZ(1)], b))
    b1 = DomainMatrix([[ZZ(1), ZZ(2)]], (1, 2), ZZ)
    raises(DMShapeError, lambda: dM.eval_poly_mul([ZZ(1)], b1))
    bq = DomainMatrix([[QQ(1)], [QQ(2)]], (2, 1), QQ)
    raises(DMDomainError, lambda: dM.eval_poly_mul([ZZ(1)], bq))

