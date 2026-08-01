
def test_has_free():
    assert x.has_free(x)
    assert not x.has_free(y)
    assert (x + y).has_free(x)
    assert (x + y).has_free(*(x, z))
    assert f(x).has_free(x)
    assert f(x).has_free(f(x))
    assert Integral(f(x), (f(x), 1, y)).has_free(y)
    assert not Integral(f(x), (f(x), 1, y)).has_free(x)
    assert not Integral(f(x), (f(x), 1, y)).has_free(f(x))
    # simple extraction
    assert (x + 1 + y).has_free(x + 1)
    assert not (x + 2 + y).has_free(x + 1)
    assert (2 + 3*x*y).has_free(3*x)
    raises(TypeError, lambda: x.has_free({x, y}))
    s = FiniteSet(1, 2)
    assert Piecewise((s, x > 3), (4, True)).has_free(s)
    assert not Piecewise((1, x > 3), (4, True)).has_free(s)
    # can't make set of these, but fallback will handle
    raises(TypeError, lambda: x.has_free(y, []))

