
def test_Module_starts_with_unity():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    B = A.submodule_from_matrix(2 * DomainMatrix.eye(4, ZZ))
    assert A.starts_with_unity() is True
    assert B.starts_with_unity() is False

