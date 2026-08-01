
def test_nsolve_rational():
    x = symbols('x')
    assert nsolve(x - Rational(1, 3), 0, prec=100) == Rational(1, 3).evalf(100)

