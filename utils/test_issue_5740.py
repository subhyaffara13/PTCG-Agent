
def test_issue_5740():
    assert limit(log(x)*z - log(2*x)*y, x, 0) == oo*sign(y - z)

