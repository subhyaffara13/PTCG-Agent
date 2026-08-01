
def test_symbolic_CentralMoment():
    mu = symbols('mu', real=True)
    sigma = symbols('sigma', positive=True)
    x = symbols('x')
    X = Normal('X', mu, sigma)
    CM = CentralMoment(X, 6)
    assert CM.rewrite(Expectation) == Expectation((X - Expectation(X))**6)
    assert CM.rewrite(Probability) == Integral((x - Integral(x*Probability(True),
                    (x, -oo, oo)))**6*Probability(Eq(X, x)), (x, -oo, oo))
    k = Dummy('k')
    expri = Integral(sqrt(2)*(k - Integral(sqrt(2)*k*exp(-(k - \
        mu)**2/(2*sigma**2))/(2*sqrt(pi)*sigma), (k, -oo, oo)))**6*exp(-(k - \
        mu)**2/(2*sigma**2))/(2*sqrt(pi)*sigma), (k, -oo, oo))
    assert CM.rewrite(Integral).dummy_eq(expri)
    assert CM.doit().simplify() == 15*sigma**6
    CM = Moment(5, 5)
    assert CM.doit() == 5**5

