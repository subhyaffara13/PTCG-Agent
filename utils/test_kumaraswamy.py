
def test_kumaraswamy():
    a = Symbol("a", positive=True)
    b = Symbol("b", positive=True)

    X = Kumaraswamy("x", a, b)
    assert density(X)(x) == x**(a - 1)*a*b*(-x**a + 1)**(b - 1)
    assert cdf(X)(x) == Piecewise((0, x < 0),
                                (-(-x**a + 1)**b + 1, x <= 1),
                                (1, True))

