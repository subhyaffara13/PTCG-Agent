
def test_issue_16714():
    assert limit(((x**(x + 1) + (x + 1)**x) / x**(x + 1))**x, x, oo) == exp(exp(1))

