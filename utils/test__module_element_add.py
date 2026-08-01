
def test_ModuleElement_add():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    C = A.submodule_from_matrix(3 * DomainMatrix.eye(4, ZZ))
    e = A(to_col([1, 2, 3, 4]), denom=6)
    f = A(to_col([5, 6, 7, 8]), denom=10)
    g = C(to_col([1, 1, 1, 1]), denom=2)
    assert e + f == A(to_col([10, 14, 18, 22]), denom=15)
    assert e - f == A(to_col([-5, -4, -3, -2]), denom=15)
    assert e + g == A(to_col([10, 11, 12, 13]), denom=6)
    assert e + QQ(7, 10) == A(to_col([26, 10, 15, 20]), denom=30)
    assert g + QQ(7, 10) == A(to_col([22, 15, 15, 15]), denom=10)

    U = Poly(cyclotomic_poly(7, x))
    Z = PowerBasis(U)
    raises(TypeError, lambda: e + Z(0))
    raises(TypeError, lambda: e + 3.14)

