
def test_issue_21038():
    assert limit(sin(pi*x)/(3*x - 12), x, 4) == pi/3

