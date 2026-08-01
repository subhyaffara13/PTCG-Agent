
def test_issue_7663():
    x = Symbol('x')
    e = '2*(x+1)'
    assert parse_expr(e, evaluate=False) == parse_expr(e, evaluate=False)
    assert parse_expr(e, evaluate=False).equals(2*(x+1))

