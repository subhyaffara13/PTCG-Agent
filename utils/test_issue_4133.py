
def test_issue_4133():
    a = sympify('Integer(4)')

    assert a == Integer(4)
    assert a.is_Integer

