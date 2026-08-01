
def test_R13():
    n, k = symbols('n k', integer=True, positive=True)
    Sm = Sum(sin(k*x), (k, 1, n))
    T = Sm.doit()  # Sum is not calculated
    assert T.simplify() == cot(x/2)/2 - cos(x*(2*n + 1)/2)/(2*sin(x/2))

