
def test_studentt():
    nu = Symbol("nu", positive=True)

    X = StudentT('x', nu)
    assert density(X)(x) == (1 + x**2/nu)**(-nu/2 - S.Half)/(sqrt(nu)*beta(S.Half, nu/2))
    assert cdf(X)(x) == S.Half + x*gamma(nu/2 + S.Half)*hyper((S.Half, nu/2 + S.Half),
                                (Rational(3, 2),), -x**2/nu)/(sqrt(pi)*sqrt(nu)*gamma(nu/2))
    raises(NotImplementedError, lambda: moment_generating_function(X))

