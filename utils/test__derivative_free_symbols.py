
def test_Derivative_free_symbols():
    f = Function('f')
    n = Symbol('n', integer=True, positive=True)
    assert diff(f(x), (x, n)).free_symbols == {n, x}

