
def test_Module_element_from_rational():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    B = A.submodule_from_matrix(2 * DomainMatrix.eye(4, ZZ))
    rA = A.element_from_rational(QQ(22, 7))
    rB = B.element_from_rational(QQ(22, 7))
    assert rA.coeffs == [22, 0, 0, 0]
    assert rA.denom == 7
    assert rA.module == A
    assert rB.coeffs == [22, 0, 0, 0]
    assert rB.denom == 7
    assert rB.module == A

