
def test_gruntz_hyperbolic():
    assert gruntz(cosh(x), x, oo) is oo
    assert gruntz(cosh(x), x, -oo) is oo
    assert gruntz(sinh(x), x, oo) is oo
    assert gruntz(sinh(x), x, -oo) is -oo
    assert gruntz(2*cosh(x)*exp(x), x, oo) is oo
    assert gruntz(2*cosh(x)*exp(x), x, -oo) == 1
    assert gruntz(2*sinh(x)*exp(x), x, oo) is oo
    assert gruntz(2*sinh(x)*exp(x), x, -oo) == -1
    assert gruntz(tanh(x), x, oo) == 1
    assert gruntz(tanh(x), x, -oo) == -1
    assert gruntz(coth(x), x, oo) == 1
    assert gruntz(coth(x), x, -oo) == -1

