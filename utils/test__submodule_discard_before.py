
def test_Submodule_discard_before():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    B = A.submodule_from_matrix(2 * DomainMatrix.eye(4, ZZ))
    B.compute_mult_tab()
    C = B.discard_before(2)
    assert C.parent == B.parent
    assert B.is_sq_maxrank_HNF() and not C.is_sq_maxrank_HNF()
    assert C.matrix == B.matrix[:, 2:]
    assert C.mult_tab() == {0: {0: [-2, -2], 1: [0, 0]}, 1: {1: [0, 0]}}

