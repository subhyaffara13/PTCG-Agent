
def test_U2():
    f = Lambda(x, Piecewise((-x, x < 0), (x, x >= 0)))
    assert diff(f(x), x) == Piecewise((-1, x < 0), (1, x >= 0))

