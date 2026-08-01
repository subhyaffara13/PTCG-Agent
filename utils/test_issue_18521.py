
def test_issue_18521():
    raises(NotImplementedError, lambda: limit(exp((2 - n) * x), x, oo))

