
def test_S10():
    k = symbols('k', integer=True, positive=True)
    Pr = Product((k*(k + 1) + 1 + I)/(k*(k + 1) + 1 - I), (k, 0, oo))
    T = Pr.doit()
    # Product does not evaluate
    assert T.simplify() == -1

