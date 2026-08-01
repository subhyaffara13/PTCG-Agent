
def test_cmath_acos():
    f = lambdify(x, acos(x), "cmath")
    assert abs(f(1) - cmath.acos(1)) < 1e-15
    assert abs(f(-1) - cmath.acos(-1)) < 1e-15
    assert abs(f(2) - cmath.acos(2)) < 1e-15
    assert abs(f(1j) - cmath.acos(1j)) < 1e-15

