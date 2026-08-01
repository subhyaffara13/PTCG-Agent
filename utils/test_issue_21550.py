
def test_issue_21550():
    r = (sqrt(5) - 1)/2
    assert limit((x - r)/(x**2 + x - 1), x, r) == sqrt(5)/5

