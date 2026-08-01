
def test_issue_6599():
    assert limit((n + cos(n))/n, n, oo) == 1

