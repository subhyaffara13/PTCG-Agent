
def test_cmath_tanh():
    f = lambdify(x, tanh(x), "cmath")
    assert abs(f(0) - cmath.tanh(0)) < 1e-15
    assert abs(f(pi) - cmath.tanh(pi)) < 1e-15
    assert abs(f(-pi) - cmath.tanh(-pi)) < 1e-15
    assert abs(f(1j) - cmath.tanh(1j)) < 1e-15

