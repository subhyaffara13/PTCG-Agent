
def test_R15():
    n, k = symbols('n k', integer=True, positive=True)
    Sm = Sum(binomial(n - k, k), (k, 0, floor(n/2)))
    T = Sm.doit()  # Sum is not calculated
    assert T.simplify() == fibonacci(n + 1)

