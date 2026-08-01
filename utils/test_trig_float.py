
def test_trig_float():
    f = lambdify([x], [cos(x), sin(x)])
    d = f(3.14159)
    assert abs(d[0] + 1) < 0.0001
    assert abs(d[1] - 0) < 0.0001

