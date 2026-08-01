
def test_discrete_probability():
    X = Geometric('X', Rational(1, 5))
    Y = Poisson('Y', 4)
    G = Geometric('e', x)
    assert P(Eq(X, 3)) == Rational(16, 125)
    assert P(X < 3) == Rational(9, 25)
    assert P(X > 3) == Rational(64, 125)
    assert P(X >= 3) == Rational(16, 25)
    assert P(X <= 3) == Rational(61, 125)
    assert P(Ne(X, 3)) == Rational(109, 125)
    assert P(Eq(Y, 3)) == 32*exp(-4)/3
    assert P(Y < 3) == 13*exp(-4)
    assert P(Y > 3).equals(32*(Rational(-71, 32) + 3*exp(4)/32)*exp(-4)/3)
    assert P(Y >= 3).equals(32*(Rational(-39, 32) + 3*exp(4)/32)*exp(-4)/3)
    assert P(Y <= 3) == 71*exp(-4)/3
    assert P(Ne(Y, 3)).equals(
        13*exp(-4) + 32*(Rational(-71, 32) + 3*exp(4)/32)*exp(-4)/3)
    assert P(X < S.Infinity) is S.One
    assert P(X > S.Infinity) is S.Zero
    assert P(G < 3) == x*(2-x)
    assert P(Eq(G, 3)) == x*(-x + 1)**2

