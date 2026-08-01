
def test_issue_22836_limit():
    assert limit(2**(1/x)/factorial(1/(x)), x, 0) == S.Zero

