
def test_issue_24751():
    expr = Add(-2, -3, evaluate=False)
    expr1 = Add(-1, expr, evaluate=False)
    assert int(expr1) == int((-3 - 2) - 1)

