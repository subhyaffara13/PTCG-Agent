
def test_ModuleElement_reduced():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    e = A(to_col([2, 4, 6, 8]), denom=2)
    f = e.reduced()
    assert f.denom == 1 and f == e

