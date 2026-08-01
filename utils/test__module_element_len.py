
def test_ModuleElement_len():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    e = A(0)
    assert len(e) == 4

