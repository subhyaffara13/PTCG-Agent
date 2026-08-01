
def test_limit2():
    assert gruntz(x**x, x, 0, dir="+") == 1
    assert gruntz((exp(x) - 1)/x, x, 0) == 1
    assert gruntz(1 + 1/x, x, oo) == 1
    assert gruntz(-exp(1/x), x, oo) == -1
    assert gruntz(x + exp(-x), x, oo) is oo
    assert gruntz(x + exp(-x**2), x, oo) is oo
    assert gruntz(x + exp(-exp(x)), x, oo) is oo
    assert gruntz(13 + 1/x - exp(-x), x, oo) == 13

