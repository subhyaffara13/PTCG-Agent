
def test_clear_coefficients():
    from sympy.simplify.simplify import clear_coefficients
    assert clear_coefficients(4*y*(6*x + 3)) == (y*(2*x + 1), 0)
    assert clear_coefficients(4*y*(6*x + 3) - 2) == (y*(2*x + 1), Rational(1, 6))
    assert clear_coefficients(4*y*(6*x + 3) - 2, x) == (y*(2*x + 1), x/12 + Rational(1, 6))
    assert clear_coefficients(sqrt(2) - 2) == (sqrt(2), 2)
    assert clear_coefficients(4*sqrt(2) - 2) == (sqrt(2), S.Half)
    assert clear_coefficients(S(3), x) == (0, x - 3)
    assert clear_coefficients(S.Infinity, x) == (S.Infinity, x)
    assert clear_coefficients(-S.Pi, x) == (S.Pi, -x)
    assert clear_coefficients(2 - S.Pi/3, x) == (pi, -3*x + 6)

