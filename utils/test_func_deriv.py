
def test_func_deriv():
    assert f(x).diff(x) == Derivative(f(x), x)
    # issue 4534
    assert f(x, y).diff(x, y) - f(x, y).diff(y, x) == 0
    assert Derivative(f(x, y), x, y).args[1:] == ((x, 1), (y, 1))
    assert Derivative(f(x, y), y, x).args[1:] == ((y, 1), (x, 1))
    assert (Derivative(f(x, y), x, y) - Derivative(f(x, y), y, x)).doit() == 0

