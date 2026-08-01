
def test_coins():
    C, D = Coin('C'), Coin('D')
    H, T = symbols('H, T')
    assert P(Eq(C, D)) == S.Half
    assert density(Tuple(C, D)) == {(H, H): Rational(1, 4), (H, T): Rational(1, 4),
            (T, H): Rational(1, 4), (T, T): Rational(1, 4)}
    assert dict(density(C).items()) == {H: S.Half, T: S.Half}

    F = Coin('F', Rational(1, 10))
    assert P(Eq(F, H)) == Rational(1, 10)

    d = pspace(C).domain

    assert d.as_boolean() == Or(Eq(C.symbol, H), Eq(C.symbol, T))

    raises(ValueError, lambda: P(C > D))  # Can't intelligently compare H to T

