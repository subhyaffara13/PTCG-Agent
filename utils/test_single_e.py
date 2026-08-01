
def test_single_e():
    f = lambdify(x, E)
    assert f(23) == exp(1.0)

