
def test_ratint_logpart():
    assert ratint_logpart(x, x**2 - 9, x, t) == \
        [(Poly(x**2 - 9, x), Poly(-2*t + 1, t))]
    assert ratint_logpart(x**2, x**3 - 5, x, t) == \
        [(Poly(x**3 - 5, x), Poly(-3*t + 1, t))]

