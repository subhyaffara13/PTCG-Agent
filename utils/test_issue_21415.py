
def test_issue_21415():
    exp = (x-1)*cos(1/(x-1))
    assert exp.limit(x,1) == 0
    assert exp.expand().limit(x,1) == 0

