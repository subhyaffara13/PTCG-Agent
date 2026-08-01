
def test_issue_14514():
    assert limit((1/(log(x)**log(x)))**(1/x), x, oo) == 1

