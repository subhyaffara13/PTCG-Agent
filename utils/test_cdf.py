
def test_cdf():
    X = Normal('x', 0, 1)

    d = cdf(X)
    assert P(X < 1) == d(1).rewrite(erfc)
    assert d(0) == S.Half

    d = cdf(X, X > 0)  # given X>0
    assert d(0) == 0

    Y = Exponential('y', 10)
    d = cdf(Y)
    assert d(-5) == 0
    assert P(Y > 3) == 1 - d(3)

    raises(ValueError, lambda: cdf(X + Y))

    Z = Exponential('z', 1)
    f = cdf(Z)
    assert f(z) == Piecewise((1 - exp(-z), z >= 0), (0, True))


def test_cdf():
    D = Die('D', 6)
    o = S.One

    assert cdf(
        D) == sympify({1: o/6, 2: o/3, 3: o/2, 4: 2*o/3, 5: 5*o/6, 6: o})

