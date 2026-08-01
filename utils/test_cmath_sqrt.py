
def test_cmath_sqrt():
    f = lambdify(x, sqrt(x), "cmath")
    assert f(0) == 0
    assert f(1) == 1
    assert f(4) == 2
    assert abs(f(2) - 1.414) < 0.001
    assert f(-1) == 1j
    assert f(-4) == 2j

