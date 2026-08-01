
def test_R18():
    k = symbols('k', integer=True, positive=True)
    Sm = Sum(1/(2**k*k**2), (k, 1, oo))
    T = Sm.doit()
    assert T.simplify() == -log(2)**2/2 + pi**2/12

