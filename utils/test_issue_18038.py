
def test_issue_18038():
    raises(AttributeError, lambda: integrate((x, x)))

