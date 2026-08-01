
def test_R16():
    k = symbols('k', integer=True, positive=True)
    Sm = Sum(1/k**2 + 1/k**3, (k, 1, oo))
    assert Sm.doit() == zeta(3) + pi**2/6

