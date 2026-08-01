
def test_issue_13425():
    assert N('2**.5', 30) == N('sqrt(2)', 30)
    assert N('x - x', 30) == 0
    assert abs((N('pi*.1', 22)*10 - pi).n()) < 1e-22

