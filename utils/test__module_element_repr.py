
def test_ModuleElement_repr():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    e = A(to_col([1, 2, 3, 4]), denom=2)
    assert repr(e) == '[1, 2, 3, 4]/2'

