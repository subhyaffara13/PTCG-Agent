
def test_cmath_acosh():
    f = lambdify(x, acosh(x), "cmath")
    assert abs(f(1) - cmath.acosh(1)) < 1e-15
    assert abs(f(2) - cmath.acosh(2)) < 1e-15
    assert abs(f(-1) - cmath.acosh(-1)) < 1e-15
    assert abs(f(2j) - cmath.acosh(2j)) < 1e-15

