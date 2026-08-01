
def test_beta_binomial():
    # verify parameters
    raises(ValueError, lambda: BetaBinomial('b', .2, 1, 2))
    raises(ValueError, lambda: BetaBinomial('b', 2, -1, 2))
    raises(ValueError, lambda: BetaBinomial('b', 2, 1, -2))
    assert BetaBinomial('b', 2, 1, 1)

    # test numeric values
    nvals = range(1,5)
    alphavals = [Rational(1, 4), S.Half, Rational(3, 4), 1, 10]
    betavals = [Rational(1, 4), S.Half, Rational(3, 4), 1, 10]

    for n in nvals:
        for a in alphavals:
            for b in betavals:
                X = BetaBinomial('X', n, a, b)
                assert E(X) == moment(X, 1)
                assert variance(X) == cmoment(X, 2)

    # test symbolic
    n, a, b = symbols('a b n')
    assert BetaBinomial('x', n, a, b)
    n = 2 # Because we're using for loops, can't do symbolic n
    a, b = symbols('a b', positive=True)
    X = BetaBinomial('X', n, a, b)
    t = Symbol('t')

    assert E(X).expand() == moment(X, 1).expand()
    assert variance(X).expand() == cmoment(X, 2).expand()
    assert skewness(X) == smoment(X, 3)
    assert characteristic_function(X)(t) == exp(2*I*t)*beta(a + 2, b)/beta(a, b) +\
         2*exp(I*t)*beta(a + 1, b + 1)/beta(a, b) + beta(a, b + 2)/beta(a, b)
    assert moment_generating_function(X)(t) == exp(2*t)*beta(a + 2, b)/beta(a, b) +\
         2*exp(t)*beta(a + 1, b + 1)/beta(a, b) + beta(a, b + 2)/beta(a, b)

