
def test_cmath_log():
    f = lambdify(x, log(x), "cmath")
    assert abs(f(1) - 0) < 1e-15
    assert abs(f(cmath.e) - 1) < 1e-15
    assert abs(f(-1) - cmath.log(-1)) < 1e-15

