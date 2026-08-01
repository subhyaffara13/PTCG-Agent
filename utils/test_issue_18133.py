
def test_issue_18133():
    assert integrate(exp(x)/(1 + x)**2, x) == NonElementaryIntegral(exp(x)/(x + 1)**2, x)

