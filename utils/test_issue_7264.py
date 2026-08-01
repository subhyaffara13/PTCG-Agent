
def test_issue_7264():
    assert integrate(exp(x)*sqrt(1 + exp(2*x))) == sqrt(exp(2*x) + 1)*exp(x)/2 + asinh(exp(x))/2

