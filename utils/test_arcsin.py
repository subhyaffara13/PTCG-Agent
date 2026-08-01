
def test_arcsin():

    a = Symbol("a", real=True)
    b = Symbol("b", real=True)

    X = Arcsin('x', a, b)
    assert density(X)(x) == 1/(pi*sqrt((-x + b)*(x - a)))
    assert cdf(X)(x) == Piecewise((0, a > x),
                            (2*asin(sqrt((-a + x)/(-a + b)))/pi, b >= x),
                            (1, True))
    assert pspace(X).domain.set == Interval(a, b)

