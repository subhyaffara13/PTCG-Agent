
def test_polygamma_expand_func():
    assert polygamma(0, x).expand(func=True) == polygamma(0, x)
    assert polygamma(0, 2*x).expand(func=True) == \
        polygamma(0, x)/2 + polygamma(0, S.Half + x)/2 + log(2)
    assert polygamma(1, 2*x).expand(func=True) == \
        polygamma(1, x)/4 + polygamma(1, S.Half + x)/4
    assert polygamma(2, x).expand(func=True) == \
        polygamma(2, x)
    assert polygamma(0, -1 + x).expand(func=True) == \
        polygamma(0, x) - 1/(x - 1)
    assert polygamma(0, 1 + x).expand(func=True) == \
        1/x + polygamma(0, x )
    assert polygamma(0, 2 + x).expand(func=True) == \
        1/x + 1/(1 + x) + polygamma(0, x)
    assert polygamma(0, 3 + x).expand(func=True) == \
        polygamma(0, x) + 1/x + 1/(1 + x) + 1/(2 + x)
    assert polygamma(0, 4 + x).expand(func=True) == \
        polygamma(0, x) + 1/x + 1/(1 + x) + 1/(2 + x) + 1/(3 + x)
    assert polygamma(1, 1 + x).expand(func=True) == \
        polygamma(1, x) - 1/x**2
    assert polygamma(1, 2 + x).expand(func=True, multinomial=False) == \
        polygamma(1, x) - 1/x**2 - 1/(1 + x)**2
    assert polygamma(1, 3 + x).expand(func=True, multinomial=False) == \
        polygamma(1, x) - 1/x**2 - 1/(1 + x)**2 - 1/(2 + x)**2
    assert polygamma(1, 4 + x).expand(func=True, multinomial=False) == \
        polygamma(1, x) - 1/x**2 - 1/(1 + x)**2 - \
        1/(2 + x)**2 - 1/(3 + x)**2
    assert polygamma(0, x + y).expand(func=True) == \
        polygamma(0, x + y)
    assert polygamma(1, x + y).expand(func=True) == \
        polygamma(1, x + y)
    assert polygamma(1, 3 + 4*x + y).expand(func=True, multinomial=False) == \
        polygamma(1, y + 4*x) - 1/(y + 4*x)**2 - \
        1/(1 + y + 4*x)**2 - 1/(2 + y + 4*x)**2
    assert polygamma(3, 3 + 4*x + y).expand(func=True, multinomial=False) == \
        polygamma(3, y + 4*x) - 6/(y + 4*x)**4 - \
        6/(1 + y + 4*x)**4 - 6/(2 + y + 4*x)**4
    assert polygamma(3, 4*x + y + 1).expand(func=True, multinomial=False) == \
        polygamma(3, y + 4*x) - 6/(y + 4*x)**4
    e = polygamma(3, 4*x + y + Rational(3, 2))
    assert e.expand(func=True) == e
    e = polygamma(3, x + y + Rational(3, 4))
    assert e.expand(func=True, basic=False) == e

    assert polygamma(-1, x, evaluate=False).expand(func=True) == \
        loggamma(x) - log(pi)/2 - log(2)/2
    p2 = polygamma(-2, x).expand(func=True) + x**2/2 - x/2 + S(1)/12
    assert isinstance(p2, Subs)
    assert p2.point == (-1,)

