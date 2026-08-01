
def test_issue_11198():
    assert factor_list(sqrt(2)*x) == (sqrt(2), [(x, 1)])
    assert factor_list(sqrt(2)*sin(x), sin(x)) == (sqrt(2), [(sin(x), 1)])

