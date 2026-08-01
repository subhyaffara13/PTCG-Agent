
def test_Poly_ltrim():
    f = Poly(y**2 + y*z**2, x, y, z).ltrim(y)
    assert f.as_expr() == y**2 + y*z**2 and f.gens == (y, z)
    assert Poly(x*y - x, z, x, y).ltrim(1) == Poly(x*y - x, x, y)

    raises(PolynomialError, lambda: Poly(x*y**2 + y**2, x, y).ltrim(y))
    raises(PolynomialError, lambda: Poly(x*y - x, x, y).ltrim(-1))

