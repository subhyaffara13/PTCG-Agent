
def test_issue_6682():
    assert gruntz(exp(2*Ei(-x))/x**2, x, 0) == exp(2*EulerGamma)


def test_issue_6682():
    assert limit(exp(2*Ei(-x))/x**2, x, 0) == exp(2*EulerGamma)


def test_issue_6682():
    # Reference value from R:
    # options(digits=16)
    # print(pnbinom(250, 50, 32/63, lower.tail=FALSE))
    assert_allclose(nbinom.sf(250, 50, 32./63.), 1.460458510976452e-35)

