
def test_issue_4547():
    assert limit(cot(x), x, 0, dir='+') is oo
    assert limit(cot(x), x, pi/2, dir='+') == 0

