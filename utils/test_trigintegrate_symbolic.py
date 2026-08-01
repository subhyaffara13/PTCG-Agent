
def test_trigintegrate_symbolic():
    n = Symbol('n', integer=True)
    assert trigintegrate(cos(x)**n, x) is None
    assert trigintegrate(sin(x)**n, x) is None
    assert trigintegrate(cot(x)**n, x) is None

