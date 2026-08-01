
def test_has_basics():
    p = Wild('p')

    assert sin(x).has(x)
    assert sin(x).has(sin)
    assert not sin(x).has(y)
    assert not sin(x).has(cos)
    assert f(x).has(x)
    assert f(x).has(f)
    assert not f(x).has(y)
    assert not f(x).has(g)

    assert f(x).diff(x).has(x)
    assert f(x).diff(x).has(f)
    assert f(x).diff(x).has(Derivative)
    assert not f(x).diff(x).has(y)
    assert not f(x).diff(x).has(g)
    assert not f(x).diff(x).has(sin)

    assert (x**2).has(Symbol)
    assert not (x**2).has(Wild)
    assert (2*p).has(Wild)

    assert not x.has()

    # see issue at https://github.com/sympy/sympy/issues/5190
    assert not S(1).has(Wild)
    assert not x.has(Wild)

