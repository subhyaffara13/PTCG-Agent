
def test_conditional_1d():
    X = Normal('x', 0, 1)
    Y = given(X, X >= 0)
    z = Symbol('z')

    assert density(Y)(z) == 2 * density(X)(z)

    assert Y.pspace.domain.set == Interval(0, oo)
    assert E(Y) == sqrt(2) / sqrt(pi)

    assert E(X**2) == E(Y**2)

