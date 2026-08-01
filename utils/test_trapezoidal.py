
def test_trapezoidal():
    a = Symbol("a", real=True)
    b = Symbol("b", real=True)
    c = Symbol("c", real=True)
    d = Symbol("d", real=True)

    X = Trapezoidal('x', a, b, c, d)
    assert density(X)(x) == Piecewise(((-2*a + 2*x)/((-a + b)*(-a - b + c + d)), (a <= x) & (x < b)),
                                      (2/(-a - b + c + d), (b <= x) & (x < c)),
                                      ((2*d - 2*x)/((-c + d)*(-a - b + c + d)), (c <= x) & (x <= d)),
                                      (0, True))

    X = Trapezoidal('x', 0, 1, 2, 3)
    assert E(X) == Rational(3, 2)
    assert variance(X) == Rational(5, 12)
    assert P(X < 2) == Rational(3, 4)
    assert median(X) == FiniteSet(Rational(3, 2))

