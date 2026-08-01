
def test_issue_6349():
    assert Float('23.e3', '')._prec == 10
    assert Float('23e3', '')._prec == 20
    assert Float('23000', '')._prec == 20
    assert Float('-23000', '')._prec == 20

