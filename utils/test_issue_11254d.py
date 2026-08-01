
def test_issue_11254d():
    # (sech(x)**2).rewrite(sinh)
    assert integrate(-1/sinh(x + I*pi/2, evaluate=False)**2, x) == -2/(exp(2*x) + 1)
    assert integrate(cosh(x)**(-2), x) == 2*tanh(x/2)/(tanh(x/2)**2 + 1)

