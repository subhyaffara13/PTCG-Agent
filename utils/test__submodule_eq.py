
def test_Submodule_eq():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    B = A.submodule_from_matrix(2 * DomainMatrix.eye(4, ZZ))
    C = A.submodule_from_matrix(6 * DomainMatrix.eye(4, ZZ), denom=3)
    assert C == B

