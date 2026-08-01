
def test_S7():
    k = symbols('k', integer=True, positive=True)
    Pr = Product((k**3 - 1)/(k**3 + 1), (k, 2, oo))
    T = Pr.doit()     # Product does not evaluate
    assert T.simplify() == R(2, 3)

