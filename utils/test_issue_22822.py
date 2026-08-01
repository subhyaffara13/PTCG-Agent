
def test_issue_22822():
    raises(ValueError, lambda: parse_expr('x', {'': 1}))
    data = {'some_parameter': None}
    assert parse_expr('some_parameter is None', data) is True

