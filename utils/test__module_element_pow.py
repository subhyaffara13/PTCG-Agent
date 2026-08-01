
def test_ModuleElement_pow():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    C = A.submodule_from_matrix(3 * DomainMatrix.eye(4, ZZ))
    e = A(to_col([0, 2, 0, 0]), denom=3)
    g = C(to_col([0, 0, 0, 1]), denom=2)
    assert e ** 3 == A(to_col([0, 0, 0, 8]), denom=27)
    assert g ** 2 == C(to_col([0, 3, 0, 0]), denom=4)
    assert e ** 0 == A(to_col([1, 0, 0, 0]))
    assert g ** 0 == A(to_col([1, 0, 0, 0]))
    assert e ** 1 == e
    assert g ** 1 == g

