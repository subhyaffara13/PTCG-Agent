
def test_sym_single_arg():
    f = lambdify(x, x * y)
    assert f(z) == z * y

