
def test_issue_5383():
    func = (1.0 * 1 + 1.0 * x)**(1.0 * 1 / x)
    assert limit(func, x, 0) == E

