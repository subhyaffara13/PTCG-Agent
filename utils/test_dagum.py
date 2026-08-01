
def test_dagum():
    p = Symbol("p", positive=True)
    b = Symbol("b", positive=True)
    a = Symbol("a", positive=True)

    X = Dagum('x', p, a, b)
    assert density(X)(x) == a*p*(x/b)**(a*p)*((x/b)**a + 1)**(-p - 1)/x
    assert cdf(X)(x) == Piecewise(((1 + (x/b)**(-a))**(-p), x >= 0),
                                    (0, True))

    p = Symbol("p", nonpositive=True)
    raises(ValueError, lambda: Dagum('x', p, a, b))

    p = Symbol("p", positive=True)
    b = Symbol("b", nonpositive=True)
    raises(ValueError, lambda: Dagum('x', p, a, b))

    b = Symbol("b", positive=True)
    a = Symbol("a", nonpositive=True)
    raises(ValueError, lambda: Dagum('x', p, a, b))
    X = Dagum('x', 1, 1, 1)
    assert median(X) == FiniteSet(1)

