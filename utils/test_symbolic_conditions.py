
def test_symbolic_conditions():
    B = Bernoulli('B', Rational(1, 4))
    D = Die('D', 4)
    b, n = symbols('b, n')
    Y = P(Eq(B, b))
    Z = E(D > n)
    assert Y == \
    Piecewise((Rational(1, 4), Eq(b, 1)), (0, True)) + \
    Piecewise((Rational(3, 4), Eq(b, 0)), (0, True))
    assert Z == \
    Piecewise((Rational(1, 4), n < 1), (0, True)) + Piecewise((S.Half, n < 2), (0, True)) + \
    Piecewise((Rational(3, 4), n < 3), (0, True)) + Piecewise((S.One, n < 4), (0, True))

