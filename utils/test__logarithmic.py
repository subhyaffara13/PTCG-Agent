
def test_Logarithmic():
    p = S.Half
    x = Logarithmic('x', p)
    assert E(x) == -p / ((1 - p) * log(1 - p))
    assert variance(x) == -1/log(2)**2 + 2/log(2)
    assert E(2*x**2 + 3*x + 4) == 4 + 7 / log(2)
    assert isinstance(E(x, evaluate=False), Expectation)

