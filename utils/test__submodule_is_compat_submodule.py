
def test_Submodule_is_compat_submodule():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    B = A.submodule_from_matrix(2 * DomainMatrix.eye(4, ZZ))
    C = A.submodule_from_matrix(3 * DomainMatrix.eye(4, ZZ))
    D = C.submodule_from_matrix(5 * DomainMatrix.eye(4, ZZ))
    assert B.is_compat_submodule(C) is True
    assert B.is_compat_submodule(A) is False
    assert B.is_compat_submodule(D) is False

