
def test_cmath_cosh():
    f = lambdify(x, cosh(x), "cmath")
    assert abs(f(0) - cmath.cosh(0)) < 1e-15
    assert abs(f(pi) - cmath.cosh(pi)) < 1e-15
    assert abs(f(-pi) - cmath.cosh(-pi)) < 1e-15
    assert abs(f(1j) - cmath.cosh(1j)) < 1e-15

