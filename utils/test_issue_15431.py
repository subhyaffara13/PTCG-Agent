
def test_issue_15431():
    assert integrate(x*exp(x)*log(x), x) == \
        (x*exp(x) - exp(x))*log(x) - exp(x) + Ei(x)

