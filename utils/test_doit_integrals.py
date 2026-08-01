
def test_doit_integrals():
    e = Integral(Integral(2*x), (x, 0, 1))
    assert e.doit() == Rational(1, 3)
    assert e.doit(deep=False) == Rational(1, 3)
    f = Function('f')
    # doesn't matter if the integral can't be performed
    assert Integral(f(x), (x, 1, 1)).doit() == 0
    # doesn't matter if the limits can't be evaluated
    assert Integral(0, (x, 1, Integral(f(x), x))).doit() == 0
    assert Integral(x, (a, 0)).doit() == 0
    limits = ((a, 1, exp(x)), (x, 0))
    assert Integral(a, *limits).doit() == Rational(1, 4)
    assert Integral(a, *list(reversed(limits))).doit() == 0

