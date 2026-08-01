
def test_R14():
    n, k = symbols('n k', integer=True, positive=True)
    Sm = Sum(sin((2*k - 1)*x), (k, 1, n))
    T = Sm.doit()  # Sum is not calculated
    assert T.simplify() == sin(n*x)**2/sin(x)

