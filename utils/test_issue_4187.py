
def test_issue_4187():
    assert integrate(log(x)*exp(-x), x) == Ei(-x) - exp(-x)*log(x)
    assert integrate(log(x)*exp(-x), (x, 0, oo)) == -EulerGamma

