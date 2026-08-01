
def test_R19():
    k = symbols('k', integer=True, positive=True)
    Sm = Sum(1/((3*k + 1)*(3*k + 2)*(3*k + 3)), (k, 0, oo))
    T = Sm.doit()
    # assert fails, T not  simplified
    assert T.simplify() == -log(3)/4 + sqrt(3)*pi/12

