
def test_symbolic_Moment():
    mu = symbols('mu', real=True)
    sigma = symbols('sigma', positive=True)
    x = symbols('x')
    X = Normal('X', mu, sigma)
    M = Moment(X, 4, 2)
    assert M.rewrite(Expectation) == Expectation((X - 2)**4)
    assert M.rewrite(Probability) == Integral((x - 2)**4*Probability(Eq(X, x)),
                                    (x, -oo, oo))
    k = Dummy('k')
    expri = Integral(sqrt(2)*(k - 2)**4*exp(-(k - \
                mu)**2/(2*sigma**2))/(2*sqrt(pi)*sigma), (k, -oo, oo))
    assert M.rewrite(Integral).dummy_eq(expri)
    assert M.doit() == (mu**4 - 8*mu**3 + 6*mu**2*sigma**2 + \
                24*mu**2 - 24*mu*sigma**2 - 32*mu + 3*sigma**4 + 24*sigma**2 + 16)
    M = Moment(2, 5)
    assert M.doit() == 2**5

