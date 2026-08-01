
def test_issue_26513():
    assert limit(abs((-x/(x+1))**x), x ,oo) == exp(-1)
    assert limit((x/(x + 1))**x, x, oo) == exp(-1)
    raises (NotImplementedError, lambda: limit((-x/(x+1))**x, x, oo))

