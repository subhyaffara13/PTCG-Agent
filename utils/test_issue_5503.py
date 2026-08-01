
def test_issue_5503():
    p = 0.5
    x = np.logspace(3, 14, 12)
    assert_allclose(binom.cdf(x, 2*x, p), 0.5, atol=1e-2)

