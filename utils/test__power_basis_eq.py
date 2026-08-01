
def test_PowerBasis_eq():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    B = PowerBasis(T)
    assert A == B

