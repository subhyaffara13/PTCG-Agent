
def test_R9():
    n, k = symbols('n k', integer=True, positive=True)
    Sm = Sum(binomial(n, k - 1)/k, (k, 1, n + 1))
    assert Sm.doit().simplify() == (2**(n + 1) - 1)/(n + 1)

