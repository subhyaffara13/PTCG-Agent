
def test_issue_18645():
    expr = And(Ge(x, 3), Le(x, 3))
    assert simplify(expr) == Eq(x, 3)
    expr = And(Eq(x, 3), Le(x, 3))
    assert simplify(expr) == Eq(x, 3)

