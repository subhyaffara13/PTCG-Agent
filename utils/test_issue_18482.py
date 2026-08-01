
def test_issue_18482():
    assert limit((2*exp(3*x)/(exp(2*x) + 1))**(1/x), x, oo) == exp(1)

