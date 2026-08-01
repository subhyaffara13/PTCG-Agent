
def test_S1():
    k = symbols('k', integer=True, positive=True)
    Pr = Product(gamma(k/3), (k, 1, 8))
    assert Pr.doit().simplify() == 640*sqrt(3)*pi**3/6561

