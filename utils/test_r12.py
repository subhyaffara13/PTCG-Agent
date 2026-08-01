
def test_R12():
    n, k = symbols('n k', integer=True, positive=True)
    Sm = Sum(fibonacci(k)**2, (k, 0, n))
    T = Sm.doit()
    assert T == fibonacci(n)*fibonacci(n + 1)

