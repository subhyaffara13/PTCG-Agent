
def test_limit3():
    a = Symbol('a')
    assert gruntz(x - log(1 + exp(x)), x, oo) == 0
    assert gruntz(x - log(a + exp(x)), x, oo) == 0
    assert gruntz(exp(x)/(1 + exp(x)), x, oo) == 1
    assert gruntz(exp(x)/(a + exp(x)), x, oo) == 1

