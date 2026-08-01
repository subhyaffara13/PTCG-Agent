
def test_issue_18747():
    assert periodicity(exp(pi*I*(x/4 + S.Half/2)), x) == 8

