
def test_issue_3609():
    assert heurisch(1/(x * (1 + log(x)**2)), x) == atan(log(x))

