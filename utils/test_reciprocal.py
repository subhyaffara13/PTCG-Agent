
def test_reciprocal():
    a = Symbol("a", real=True)
    b = Symbol("b", real=True)

    X = Reciprocal('x', a, b)
    assert density(X)(x) == 1/(x*(-log(a) + log(b)))
    assert cdf(X)(x) == Piecewise((log(a)/(log(a) - log(b)) - log(x)/(log(a) - log(b)), a <= x), (0, True))
    X = Reciprocal('x', 5, 30)

    assert E(X) == 25/(log(30) - log(5))
    assert P(X < 4) == S.Zero
    assert P(X < 20) == log(20) / (log(30) - log(5)) - log(5) / (log(30) - log(5))
    assert cdf(X)(10) == log(10) / (log(30) - log(5)) - log(5) / (log(30) - log(5))

    a = symbols('a', nonpositive=True)
    raises(ValueError, lambda: Reciprocal('x', a, b))

    a = symbols('a', positive=True)
    b = symbols('b', positive=True)
    raises(ValueError, lambda: Reciprocal('x', a + b, a))

