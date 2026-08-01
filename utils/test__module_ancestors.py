
def test_Module_ancestors():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    B = A.submodule_from_matrix(2 * DomainMatrix.eye(4, ZZ))
    C = B.submodule_from_matrix(3 * DomainMatrix.eye(4, ZZ))
    D = B.submodule_from_matrix(5 * DomainMatrix.eye(4, ZZ))
    assert C.ancestors(include_self=True) == [A, B, C]
    assert D.ancestors(include_self=True) == [A, B, D]
    assert C.power_basis_ancestor() == A
    assert C.nearest_common_ancestor(D) == B
    M = Module()
    assert M.power_basis_ancestor() is None

