
def test_FiniteRV():
    F = FiniteRV('F', {1: S.Half, 2: Rational(1, 4), 3: Rational(1, 4)}, check=True)
    p = Symbol("p", positive=True)

    assert dict(density(F).items()) == {S.One: S.Half, S(2): Rational(1, 4), S(3): Rational(1, 4)}
    assert P(F >= 2) == S.Half
    assert quantile(F)(p) == Piecewise((nan, p > S.One), (S.One, p <= S.Half),\
        (S(2), p <= Rational(3, 4)),(S(3), True))

    assert pspace(F).domain.as_boolean() == Or(
        *[Eq(F.symbol, i) for i in [1, 2, 3]])

    assert F.pspace.domain.set == FiniteSet(1, 2, 3)
    raises(ValueError, lambda: FiniteRV('F', {1: S.Half, 2: S.Half, 3: S.Half}, check=True))
    raises(ValueError, lambda: FiniteRV('F', {1: S.Half, 2: Rational(-1, 2), 3: S.One}, check=True))
    raises(ValueError, lambda: FiniteRV('F', {1: S.One, 2: Rational(3, 2), 3: S.Zero,\
        4: Rational(-1, 2), 5: Rational(-3, 4), 6: Rational(-1, 4)}, check=True))

    # purposeful invalid pmf but it should not raise since check=False
    # see test_drv_types.test_ContinuousRV for explanation
    X = FiniteRV('X', {1: 1, 2: 2})
    assert E(X) == 5
    assert P(X <= 2) + P(X > 2) != 1

