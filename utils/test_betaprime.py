
def test_betaprime():
    alpha = Symbol("alpha", positive=True)

    betap = Symbol("beta", positive=True)

    X = BetaPrime('x', alpha, betap)
    assert density(X)(x) == x**(alpha - 1)*(x + 1)**(-alpha - betap)/beta(alpha, betap)

    alpha = Symbol("alpha", nonpositive=True)
    raises(ValueError, lambda: BetaPrime('x', alpha, betap))

    alpha = Symbol("alpha", positive=True)
    betap = Symbol("beta", nonpositive=True)
    raises(ValueError, lambda: BetaPrime('x', alpha, betap))
    X = BetaPrime('x', 1, 1)
    assert median(X) == FiniteSet(1)

