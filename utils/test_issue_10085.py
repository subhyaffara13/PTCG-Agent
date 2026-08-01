
def test_issue_10085():
    assert invert_real(exp(x),0,x) == (x, S.EmptySet)

