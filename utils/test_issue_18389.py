
def test_issue_18389():
    n = Symbol("n", integer=True)
    expr = Eq(n, 0) | (n >= 1)
    assert simplify(expr) == Ge(n, 0)

