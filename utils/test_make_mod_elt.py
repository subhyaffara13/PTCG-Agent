
def test_make_mod_elt():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    B = A.submodule_from_matrix(2 * DomainMatrix.eye(4, ZZ))
    col = to_col([1, 2, 3, 4])
    eA = make_mod_elt(A, col)
    eB = make_mod_elt(B, col)
    assert isinstance(eA, PowerBasisElement)
    assert not isinstance(eB, PowerBasisElement)

