
def test_PowerBasisElement_polys():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    e = A(to_col([1, 15, 8, 0]), denom=2)
    assert e.numerator(x=zeta) == Poly(8 * zeta ** 2 + 15 * zeta + 1, domain=ZZ)
    assert e.poly(x=zeta) == Poly(4 * zeta ** 2 + QQ(15, 2) * zeta + QQ(1, 2), domain=QQ)

