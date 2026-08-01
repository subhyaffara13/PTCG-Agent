
def test_cmath_sin():
    f = lambdify(x, sin(x), "cmath")
    assert abs(f(0) - cmath.sin(0)) < 1e-15
    assert abs(f(pi) - cmath.sin(pi)) < 1e-15
    assert abs(f(-pi) - cmath.sin(-pi)) < 1e-15
    assert abs(f(1j) - cmath.sin(1j)) < 1e-15

