
def test_given():
    X = Die('X', 6)
    assert density(X, X > 5) == {S(6): S.One}
    assert where(X > 2, X > 5).as_boolean() == Eq(X.symbol, 6)


def test_given():
    X = Normal('X', 0, 1)
    Y = Normal('Y', 0, 1)
    A = given(X, True)
    B = given(X, Y > 2)

    assert X == A == B

