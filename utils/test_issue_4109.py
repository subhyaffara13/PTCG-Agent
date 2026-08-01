
def test_issue_4109():
    assert gruntz(1/gamma(x), x, 0) == 0
    assert gruntz(x*gamma(x), x, 0) == 1

