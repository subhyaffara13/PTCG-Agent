
def test_S8():
    k = symbols('k', integer=True, positive=True)
    Pr = Product(1 - 1/(2*k)**2, (k, 1, oo))
    T = Pr.doit()
    # Product does not evaluate
    assert T.simplify() == 2/pi

