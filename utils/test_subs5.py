
def test_subs5():
    e = Integral(exp(-x**2), (x, -oo, oo))
    assert e.subs(x, 5) == e
    e = Integral(exp(-x**2 + y), x)
    assert e.subs(y, 5) == Integral(exp(-x**2 + 5), x)
    e = Integral(exp(-x**2 + y), (x, x))
    assert e.subs(x, 5) == Integral(exp(y - x**2), (x, 5))
    assert e.subs(y, 5) == Integral(exp(-x**2 + 5), x)
    e = Integral(exp(-x**2 + y), (y, -oo, oo), (x, -oo, oo))
    assert e.subs(x, 5) == e
    assert e.subs(y, 5) == e
    # Test evaluation of antiderivatives
    e = Integral(exp(-x**2), (x, x))
    assert e.subs(x, 5) == Integral(exp(-x**2), (x, 5))
    e = Integral(exp(x), x)
    assert (e.subs(x,1) - e.subs(x,0) - Integral(exp(x), (x, 0, 1))
        ).doit().is_zero

