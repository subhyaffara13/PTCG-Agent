
def test_conditional():
    X = Geometric('X', Rational(2, 3))
    Y = Poisson('Y', 3)
    assert P(X > 2, X > 3) == 1
    assert P(X > 3, X > 2) == Rational(1, 3)
    assert P(Y > 2, Y < 2) == 0
    assert P(Eq(Y, 3), Y >= 0) == 9*exp(-3)/2
    assert P(Eq(Y, 3), Eq(Y, 2)) == 0
    assert P(X < 2, Eq(X, 2)) == 0
    assert P(X > 2, Eq(X, 3)) == 1

