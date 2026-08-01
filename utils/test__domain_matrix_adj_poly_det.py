
def test_DomainMatrix_adj_poly_det():
    A = DM([[ZZ(1), ZZ(2), ZZ(3)],
            [ZZ(4), ZZ(5), ZZ(6)],
            [ZZ(7), ZZ(8), ZZ(9)]], ZZ)
    p, detA = A.adj_poly_det()
    assert p == [ZZ(1), ZZ(-15), ZZ(-18)]
    assert A.adjugate() == p[0]*A**2 + p[1]*A**1 + p[2]*A**0 == A.eval_poly(p)
    assert A.det() == detA

    A = DM([[ZZ(1), ZZ(2), ZZ(3)],
            [ZZ(7), ZZ(8), ZZ(9)]], ZZ)
    raises(DMNonSquareMatrixError, lambda: A.adj_poly_det())

