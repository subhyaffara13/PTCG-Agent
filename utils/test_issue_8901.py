
def test_issue_8901():
    assert integrate(sinh(1.0*x)) == 1.0*cosh(1.0*x)
    assert integrate(tanh(1.0*x)) == 1.0*x - 1.0*log(tanh(1.0*x) + 1)
    assert integrate(tanh(x)) == x - log(tanh(x) + 1)

