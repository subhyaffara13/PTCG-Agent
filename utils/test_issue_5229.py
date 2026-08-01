
def test_issue_5229():
    assert limit((1 + y)**(1/y) - S.Exp1, y, 0) == 0

