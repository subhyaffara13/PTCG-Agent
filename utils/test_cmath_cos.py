
def test_cmath_cos():
    f = lambdify(x, cos(x), "cmath")
    assert abs(f(0) - cmath.cos(0)) < 1e-15
    assert abs(f(pi) - cmath.cos(pi)) < 1e-15
    assert abs(f(-pi) - cmath.cos(-pi)) < 1e-15
    assert abs(f(1j) - cmath.cos(1j)) < 1e-15

