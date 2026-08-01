
def test_subs7():
    e = Integral(x, (x, 1, y), (y, 1, 2))
    assert e.subs({x: 1, y: 2}) == e
    e = Integral(sin(x) + sin(y), (x, sin(x), sin(y)),
                                  (y, 1, 2))
    assert e.subs(sin(y), 1) == e
    assert e.subs(sin(x), 1) == Integral(sin(x) + sin(y), (x, 1, sin(y)),
                                         (y, 1, 2))

