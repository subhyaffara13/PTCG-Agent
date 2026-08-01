
def test_subs6():
    a, b = symbols('a b')
    e = Integral(x*y, (x, f(x), f(y)))
    assert e.subs(x, 1) == Integral(x*y, (x, f(1), f(y)))
    assert e.subs(y, 1) == Integral(x, (x, f(x), f(1)))
    e = Integral(x*y, (x, f(x), f(y)), (y, f(x), f(y)))
    assert e.subs(x, 1) == Integral(x*y, (x, f(1), f(y)), (y, f(1), f(y)))
    assert e.subs(y, 1) == Integral(x*y, (x, f(x), f(y)), (y, f(x), f(1)))
    e = Integral(x*y, (x, f(x), f(a)), (y, f(x), f(a)))
    assert e.subs(a, 1) == Integral(x*y, (x, f(x), f(1)), (y, f(x), f(1)))

