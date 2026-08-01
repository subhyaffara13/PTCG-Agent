
def test_issue_5126():
    assert (-2)**x*(-3)**x != 6**x
    i = Symbol('i', integer=1)
    assert (-2)**i*(-3)**i == 6**i

