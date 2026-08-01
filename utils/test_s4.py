
def test_S4():
    n, k = symbols('n k', integer=True, positive=True)
    assert Product(1 + 1/k, (k, 1, n -1)).doit().simplify() == n

