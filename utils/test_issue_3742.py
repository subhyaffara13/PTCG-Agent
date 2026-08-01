
def test_issue_3742():
    e = sqrt(x)*exp(y)
    assert e.subs(sqrt(x), 1) == exp(y)

