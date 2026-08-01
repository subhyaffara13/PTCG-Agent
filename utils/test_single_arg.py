
def test_single_arg():
    f = lambdify(x, 2*x)
    assert f(1) == 2

