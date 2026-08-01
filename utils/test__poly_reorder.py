
def test_Poly_reorder():
    raises(PolynomialError, lambda: Poly(x + y).reorder(x, z))

    assert Poly(x + y, x, y).reorder(x, y) == Poly(x + y, x, y)
    assert Poly(x + y, x, y).reorder(y, x) == Poly(x + y, y, x)

    assert Poly(x + y, y, x).reorder(x, y) == Poly(x + y, x, y)
    assert Poly(x + y, y, x).reorder(y, x) == Poly(x + y, y, x)

    assert Poly(x + y, x, y).reorder(wrt=x) == Poly(x + y, x, y)
    assert Poly(x + y, x, y).reorder(wrt=y) == Poly(x + y, y, x)

