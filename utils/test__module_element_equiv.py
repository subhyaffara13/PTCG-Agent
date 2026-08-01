
def test_ModuleElement_equiv():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    e = A(to_col([1, 2, 3, 4]), denom=1)
    f = A(to_col([3, 6, 9, 12]), denom=3)
    assert e.equiv(f)

    C = A.submodule_from_matrix(3 * DomainMatrix.eye(4, ZZ))
    g = C(to_col([1, 2, 3, 4]), denom=1)
    h = A(to_col([3, 6, 9, 12]), denom=1)
    assert g.equiv(h)
    assert C(to_col([5, 0, 0, 0]), denom=7).equiv(QQ(15, 7))

    U = Poly(cyclotomic_poly(7, x))
    Z = PowerBasis(U)
    raises(UnificationFailed, lambda: e.equiv(Z(0)))

    assert e.equiv(3.14) is False

