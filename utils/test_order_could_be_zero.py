
def test_order_could_be_zero():
    x, y = symbols('x, y')
    n = symbols('n', integer=True, nonnegative=True)
    m = symbols('m', integer=True, positive=True)
    assert diff(y, (x, n)) == Piecewise((y, Eq(n, 0)), (0, True))
    assert diff(y, (x, n + 1)) is S.Zero
    assert diff(y, (x, m)) is S.Zero

