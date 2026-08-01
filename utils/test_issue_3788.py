
def test_issue_3788():
    assert integrate(1/(1 + x**2), x) == atan(x)

