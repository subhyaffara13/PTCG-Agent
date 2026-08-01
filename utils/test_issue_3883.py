
def test_issue_3883():
    from sympy.abc import gamma, mu, x
    f = (-gamma * (x - mu)**2 - log(gamma) + log(2*pi))/2
    a, b, c = symbols('a b c', cls=Wild, exclude=(gamma,))

    assert f.match(a * log(gamma) + b * gamma + c) == \
        {a: Rational(-1, 2), b: -(-mu + x)**2/2, c: log(2*pi)/2}
    assert f.expand().collect(gamma).match(a * log(gamma) + b * gamma + c) == \
        {a: Rational(-1, 2), b: (-(x - mu)**2/2).expand(), c: (log(2*pi)/2).expand()}
    g1 = Wild('g1', exclude=[gamma])
    g2 = Wild('g2', exclude=[gamma])
    g3 = Wild('g3', exclude=[gamma])
    assert f.expand().match(g1 * log(gamma) + g2 * gamma + g3) == \
    {g3: log(2)/2 + log(pi)/2, g1: Rational(-1, 2), g2: -mu**2/2 + mu*x - x**2/2}

