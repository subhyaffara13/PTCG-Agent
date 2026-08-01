
def test_ContinuousDomain():
    X = Normal('x', 0, 1)
    assert where(X**2 <= 1).set == Interval(-1, 1)
    assert where(X**2 <= 1).symbol == X.symbol
    assert where(And(X**2 <= 1, X >= 0)).set == Interval(0, 1)
    raises(ValueError, lambda: where(sin(X) > 1))

    Y = given(X, X >= 0)

    assert Y.pspace.domain.set == Interval(0, oo)

