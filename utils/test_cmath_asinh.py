
def test_cmath_asinh():
    f = lambdify(x, asinh(x), "cmath")
    assert abs(f(0) - cmath.asinh(0)) < 1e-15
    assert abs(f(1) - cmath.asinh(1)) < 1e-15
    assert abs(f(-1) - cmath.asinh(-1)) < 1e-15
    assert abs(f(2) - cmath.asinh(2)) < 1e-15
    assert abs(f(2j) - cmath.asinh(2j)) < 1e-15

