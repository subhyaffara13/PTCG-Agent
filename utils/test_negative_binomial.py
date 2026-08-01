
def test_negative_binomial():
    r = 5
    p = S.One / 3
    x = NegativeBinomial('x', r, p)
    assert E(x) == r * (1 - p) / p
    # This hangs when run with the cache disabled:
    assert variance(x) == r * (1 - p) / p**2
    assert E(x**5 + 2*x + 3) == E(x**5) + 2*E(x) + 3 == Rational(796473, 1)
    assert isinstance(E(x, evaluate=False), Expectation)

