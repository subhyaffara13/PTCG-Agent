
def test_cmath_atan():
    f = lambdify(x, atan(x), "cmath")
    assert abs(f(0) - cmath.atan(0)) < 1e-15
    assert abs(f(1) - cmath.atan(1)) < 1e-15
    assert abs(f(-1) - cmath.atan(-1)) < 1e-15
    assert abs(f(2) - cmath.atan(2)) < 1e-15
    assert abs(f(2j) - cmath.atan(2j)) < 1e-15

