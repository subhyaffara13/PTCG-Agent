
def test_DomainMatrix_eval_poly():
    dM = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    p = [ZZ(1), ZZ(2), ZZ(3)]
    result = DomainMatrix([[ZZ(12), ZZ(14)], [ZZ(21), ZZ(33)]], (2, 2), ZZ)
    assert dM.eval_poly(p) == result == p[0]*dM**2 + p[1]*dM + p[2]*dM**0
    assert dM.eval_poly([]) == dM.zeros(dM.shape, dM.domain)
    assert dM.eval_poly([ZZ(2)]) == 2*dM.eye(2, dM.domain)

    dM2 = DomainMatrix([[ZZ(1), ZZ(2)]], (1, 2), ZZ)
    raises(DMNonSquareMatrixError, lambda: dM2.eval_poly([ZZ(1)]))

