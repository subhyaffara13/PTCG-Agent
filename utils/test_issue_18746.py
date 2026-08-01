
def test_issue_18746():
    e3 = cos(S.Pi*(x/4 + 1/4))
    assert e3.period() == 8

