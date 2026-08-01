
def test_PowerBasisElement_inverse():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    e = A(to_col([1, 1, 1, 1]))
    assert 2 // e == -2*A(1)
    assert e ** -3 == -A(3)

