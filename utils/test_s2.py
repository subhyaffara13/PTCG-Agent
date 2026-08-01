
def test_S2():
    n, k = symbols('n k', integer=True, positive=True)
    assert Product(k, (k, 1, n)).doit() == factorial(n)

