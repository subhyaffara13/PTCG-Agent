
def test_cmath_sinh():
    f = lambdify(x, sinh(x), "cmath")
    assert abs(f(0) - cmath.sinh(0)) < 1e-15
    assert abs(f(pi) - cmath.sinh(pi)) < 1e-15
    assert abs(f(-pi) - cmath.sinh(-pi)) < 1e-15
    assert abs(f(1j) - cmath.sinh(1j)) < 1e-15

