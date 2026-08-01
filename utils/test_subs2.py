
def test_subs2():
    e = Integral(exp(x - y), x, t)
    assert e.subs(y, 3) == Integral(exp(x - 3), x, t)
    e = Integral(exp(x - y), (x, 0, 1), (t, 0, 1))
    assert e.subs(y, 3) == Integral(exp(x - 3), (x, 0, 1), (t, 0, 1))
    f = Lambda(x, exp(-x**2))
    conv = Integral(f(x - y)*f(y), (y, -oo, oo), (t, 0, 1))
    assert conv.subs({x: 0}) == Integral(exp(-2*y**2), (y, -oo, oo), (t, 0, 1))

