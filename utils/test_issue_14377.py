
def test_issue_14377():
    raises(NotImplementedError, lambda: limit(exp(I*x)*sin(pi*x), x, oo))

