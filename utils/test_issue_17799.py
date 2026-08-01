
def test_issue_17799():
    assert solve(-erf(x**(S(1)/3))**pi + I, x) == []

