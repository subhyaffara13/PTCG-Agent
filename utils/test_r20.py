
def test_R20():
    n, k = symbols('n k', integer=True, positive=True)
    Sm = Sum(binomial(n, 4*k), (k, 0, oo))
    T = Sm.doit()
    # assert fails, T not  simplified
    assert T.simplify() == 2**(n/2)*cos(pi*n/4)/2 + 2**(n - 1)/2

