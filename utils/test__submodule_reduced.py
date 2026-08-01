
def test_Submodule_reduced():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    B = A.submodule_from_matrix(2 * DomainMatrix.eye(4, ZZ))
    C = A.submodule_from_matrix(6 * DomainMatrix.eye(4, ZZ), denom=3)
    D = C.reduced()
    assert D.denom == 1 and D == C == B

