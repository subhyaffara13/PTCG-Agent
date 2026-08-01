
def test_Poly_exclude():
    assert Poly(x, x, y).exclude() == Poly(x, x)
    assert Poly(x*y, x, y).exclude() == Poly(x*y, x, y)
    assert Poly(1, x, y).exclude() == Poly(1, x, y)

