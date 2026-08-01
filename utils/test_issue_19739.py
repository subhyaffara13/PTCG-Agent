
def test_issue_19739():
    assert limit((-S(1)/4)**x, x, oo) == 0

