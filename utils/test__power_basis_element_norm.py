
def test_PowerBasisElement_norm():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    lam = A(to_col([1, -1, 0, 0]))
    assert lam.norm() == 5

