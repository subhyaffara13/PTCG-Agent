
def test_limit1():
    assert gruntz(x, x, oo) is oo
    assert gruntz(x, x, -oo) is -oo
    assert gruntz(-x, x, oo) is -oo
    assert gruntz(x**2, x, -oo) is oo
    assert gruntz(-x**2, x, oo) is -oo
    assert gruntz(x*log(x), x, 0, dir="+") == 0
    assert gruntz(1/x, x, oo) == 0
    assert gruntz(exp(x), x, oo) is oo
    assert gruntz(-exp(x), x, oo) is -oo
    assert gruntz(exp(x)/x, x, oo) is oo
    assert gruntz(1/x - exp(-x), x, oo) == 0
    assert gruntz(x + 1/x, x, oo) is oo

