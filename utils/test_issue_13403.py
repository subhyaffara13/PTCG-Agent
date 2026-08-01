
def test_issue_13403():
    assert limit(x*(-1 + (x + log(x + 1) + 1)/(x + log(x))), x, oo) == 1

