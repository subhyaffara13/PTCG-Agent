
def test_coeff_expand():
    expr = z*(x + y)**2
    expr2 = z*(x + y)**2 + z*(2*x + 2*y)**2
    assert expr.coeff(z) == (x + y)**2
    assert expr2.coeff(z) == (x + y)**2 + (2*x + 2*y)**2

