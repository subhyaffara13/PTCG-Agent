
def test_R21():
    k = symbols('k', integer=True, positive=True)
    Sm = Sum(1/(sqrt(k*(k + 1)) * (sqrt(k) + sqrt(k + 1))), (k, 1, oo))
    T = Sm.doit()  # Sum not calculated
    assert T.simplify() == 1

