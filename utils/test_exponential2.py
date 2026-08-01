
def test_exponential2():
    n = Symbol('n')
    assert limit((1 + x/(n + sin(n)))**n, n, oo) == exp(x)

