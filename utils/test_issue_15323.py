
def test_issue_15323():
    d = ((1 - 1/x)**x).diff(x)
    assert limit(d, x, 1, dir='+') == 1

