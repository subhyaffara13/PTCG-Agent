
def test_R8():
    n, k = symbols('n k', integer=True, positive=True)
    Sm = Sum(k**2*binomial(n, k), (k, 1, n))
    T = Sm.doit() #returns Piecewise function
    assert T.combsimp() == n*(n + 1)*2**(n - 2)

