
def test_S9():
    k = symbols('k', integer=True, positive=True)
    Pr = Product(1 + (-1)**(k + 1)/(2*k - 1), (k, 1, oo))
    T = Pr.doit()
    # Product produces 0
    # https://github.com/sympy/sympy/issues/7133
    assert T.simplify() == sqrt(2)

