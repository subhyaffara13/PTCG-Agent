
def test_PowerBasis_repr():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    assert repr(A) == 'PowerBasis(x**4 + x**3 + x**2 + x + 1)'

