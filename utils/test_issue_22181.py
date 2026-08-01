
def test_issue_22181():
    assert limit((-1)**x * 2**(-x), x, oo) == 0

