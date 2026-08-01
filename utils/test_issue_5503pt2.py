
def test_issue_5503pt2(x, n, p, cdf_desired):
    assert_allclose(binom.cdf(x, n, p), cdf_desired)

