
def test_issue_9585():
    assert diff(Poly(x**2 + x)) == Poly(2*x + 1)
    assert diff(Poly(x**2 + x), x, evaluate=False) == \
        Derivative(Poly(x**2 + x), x)
    assert Derivative(Poly(x**2 + x), x).doit() == Poly(2*x + 1)

