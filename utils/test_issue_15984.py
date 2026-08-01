
def test_issue_15984():
    assert limit((-x + log(exp(x) + 1))/x, x, oo, dir='-') == 0

