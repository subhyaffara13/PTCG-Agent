
def test_parse_function_issue_3539():
    x = Symbol('x')
    f = Function('f')
    assert parse_expr('f(x)') == f(x)

