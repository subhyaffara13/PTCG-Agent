
def test_R7():
    n, k = symbols('n k', integer=True, positive=True)
    T = Sum(k**3,(k,1,n)).doit()
    assert T.factor() == n**2*(n + 1)**2/4

