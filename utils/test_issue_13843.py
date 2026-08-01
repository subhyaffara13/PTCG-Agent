
def test_issue_13843():
    x = symbols('x')
    f = Function('f')
    m, n = symbols('m n', integer=True)
    assert Derivative(Derivative(f(x), (x, m)), (x, n)) == Derivative(f(x), (x, m + n))
    assert Derivative(Derivative(f(x), (x, m+5)), (x, n+3)) == Derivative(f(x), (x, m + n + 8))

    assert Derivative(f(x), (x, n)).doit() == Derivative(f(x), (x, n))

