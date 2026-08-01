
def test_pareto_numeric():
    xm, beta = 3, 2
    alpha = beta + 5
    X = Pareto('x', xm, alpha)

    assert E(X) == alpha*xm/S(alpha - 1)
    assert variance(X) == xm**2*alpha / S((alpha - 1)**2*(alpha - 2))
    assert median(X) == FiniteSet(3*2**Rational(1, 7))

