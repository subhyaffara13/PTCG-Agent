
def test_issue_4190():
    assert gruntz(x - gamma(1/x), x, oo) == S.EulerGamma

