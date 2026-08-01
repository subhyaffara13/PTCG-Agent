
def test_issue_5436():
    raises(NotImplementedError, lambda: limit(exp(x*y), x, oo))
    raises(NotImplementedError, lambda: limit(exp(-x*y), x, oo))

