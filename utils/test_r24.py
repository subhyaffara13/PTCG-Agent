
def test_R24():
    m, k = symbols('m k', integer=True, positive=True)
    Sm = Sum(Product(k/(2*k - 1), (k, 1, m)), (m, 2, oo))
    assert Sm.doit() == pi/2

