
def test_ModuleElement_column():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    e = A(0)
    col1 = e.column()
    assert col1 == e.col and col1 is not e.col
    col2 = e.column(domain=FF(5))
    assert col2.domain.is_FF

