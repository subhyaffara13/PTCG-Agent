
def test_binomial_quantile():
    X = Binomial('X', 50, S.Half)
    assert quantile(X)(0.95) == S(31)
    assert median(X) == FiniteSet(25)

    X = Binomial('X', 5, S.Half)
    p = Symbol("p", positive=True)
    assert quantile(X)(p) == Piecewise((nan, p > S.One), (S.Zero, p <= Rational(1, 32)),\
        (S.One, p <= Rational(3, 16)), (S(2), p <= S.Half), (S(3), p <= Rational(13, 16)),\
        (S(4), p <= Rational(31, 32)), (S(5), p <= S.One))
    assert median(X) == FiniteSet(2, 3)

