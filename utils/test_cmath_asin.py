
def test_cmath_asin():
    f = lambdify(x, asin(x), "cmath")
    assert abs(f(0) - cmath.asin(0)) < 1e-15
    assert abs(f(1) - cmath.asin(1)) < 1e-15
    assert abs(f(-1) - cmath.asin(-1)) < 1e-15
    assert abs(f(2) - cmath.asin(2)) < 1e-15
    assert abs(f(1j) - cmath.asin(1j)) < 1e-15

