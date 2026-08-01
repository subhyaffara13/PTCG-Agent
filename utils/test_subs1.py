
def test_subs1():
    e = Integral(exp(x - y), x)
    assert e.subs(y, 3) == Integral(exp(x - 3), x)
    e = Integral(exp(x - y), (x, 0, 1))
    assert e.subs(y, 3) == Integral(exp(x - 3), (x, 0, 1))
    f = Lambda(x, exp(-x**2))
    conv = Integral(f(x - y)*f(y), (y, -oo, oo))
    assert conv.subs({x: 0}) == Integral(exp(-2*y**2), (y, -oo, oo))

