
def test_cmath_tan():
    f = lambdify(x, tan(x), "cmath")
    assert abs(f(0) - cmath.tan(0)) < 1e-15
    assert abs(f(1j) - cmath.tan(1j)) < 1e-15

