
def test_issue_8634():
    n = Symbol('n', integer=True, positive=True)
    x = Symbol('x')
    assert limit(x**n, x, -oo) == oo*sign((-1)**n)

