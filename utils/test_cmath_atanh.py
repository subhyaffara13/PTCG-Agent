
def test_cmath_atanh():
    f = lambdify(x, atanh(x), "cmath")
    assert abs(f(0) - cmath.atanh(0)) < 1e-15
    assert abs(f(0.5) - cmath.atanh(0.5)) < 1e-15
    assert abs(f(-0.5) - cmath.atanh(-0.5)) < 1e-15
    assert abs(f(2) - cmath.atanh(2)) < 1e-15
    assert abs(f(-2) - cmath.atanh(-2)) < 1e-15
    assert abs(f(2j) - cmath.atanh(2j)) < 1e-15

