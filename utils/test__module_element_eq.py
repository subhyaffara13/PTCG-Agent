
def test_ModuleElement_eq():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    e = A(to_col([1, 2, 3, 4]), denom=1)
    f = A(to_col([3, 6, 9, 12]), denom=3)
    assert e == f

    U = Poly(cyclotomic_poly(7, x))
    Z = PowerBasis(U)
    assert e != Z(0)
    assert e != 3.14

