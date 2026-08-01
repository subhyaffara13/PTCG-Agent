
def test_Poly_precision():
    # Make sure Poly doesn't lose precision
    p = Poly(pi.evalf(100)*x)
    assert p.as_expr() == pi.evalf(100)*x

