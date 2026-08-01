
def test_issue_19822():
    expr = And(Gt(n-2, 1), Gt(n, 1))
    assert simplify(expr) == Gt(n, 3)

