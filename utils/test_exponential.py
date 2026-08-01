
def test_exponential():
    rate = Symbol('lambda', positive=True)
    X = Exponential('x', rate)
    p = Symbol("p", positive=True, real=True)

    assert E(X) == 1/rate
    assert variance(X) == 1/rate**2
    assert skewness(X) == 2
    assert skewness(X) == smoment(X, 3)
    assert kurtosis(X) == 9
    assert kurtosis(X) == smoment(X, 4)
    assert smoment(2*X, 4) == smoment(X, 4)
    assert moment(X, 3) == 3*2*1/rate**3
    assert P(X > 0) is S.One
    assert P(X > 1) == exp(-rate)
    assert P(X > 10) == exp(-10*rate)
    assert quantile(X)(p) == -log(1-p)/rate

    assert where(X <= 1).set == Interval(0, 1)
    Y = Exponential('y', 1)
    assert median(Y) == FiniteSet(log(2))
    #Test issue 9970
    z = Dummy('z')
    assert P(X > z) == exp(-z*rate)
    assert P(X < z) == 0
    #Test issue 10076 (Distribution with interval(0,oo))
    x = Symbol('x')
    _z = Dummy('_z')
    b = SingleContinuousPSpace(x, ExponentialDistribution(2))

    with ignore_warnings(UserWarning): ### TODO: Restore tests once warnings are removed
        expected1 = Integral(2*exp(-2*_z), (_z, 3, oo))
        assert b.probability(x > 3, evaluate=False).rewrite(Integral).dummy_eq(expected1)

        expected2 = Integral(2*exp(-2*_z), (_z, 0, 4))
        assert b.probability(x < 4, evaluate=False).rewrite(Integral).dummy_eq(expected2)
    Y = Exponential('y', 2*rate)
    assert coskewness(X, X, X) == skewness(X)
    assert coskewness(X, Y + rate*X, Y + 2*rate*X) == \
                        4/(sqrt(1 + 1/(4*rate**2))*sqrt(4 + 1/(4*rate**2)))
    assert coskewness(X + 2*Y, Y + X, Y + 2*X, X > 3) == \
                        sqrt(170)*Rational(9, 85)


def test_exponential():
    n = Symbol('n')
    x = Symbol('x', real=True)
    assert limit((1 + x/n)**n, n, oo) == exp(x)
    assert limit((1 + x/(2*n))**n, n, oo) == exp(x/2)
    assert limit((1 + x/(2*n + 1))**n, n, oo) == exp(x/2)
    assert limit(((x - 1)/(x + 1))**x, x, oo) == exp(-2)
    assert limit(1 + (1 + 1/x)**x, x, oo) == 1 + S.Exp1
    assert limit((2 + 6*x)**x/(6*x)**x, x, oo) == exp(S('1/3'))


def test_exponential(xp):
    for k, v in exponential_data.items():
        if v is None:
            assert_raises(ValueError, windows.exponential, *k, xp=xp)
        else:
            win = windows.exponential(*k, xp=xp)
            xp_assert_close(win, xp.asarray(v), rtol=1e-14)

