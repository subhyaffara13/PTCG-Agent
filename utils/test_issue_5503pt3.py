
def test_issue_5503pt3():
    # From Wolfram Alpha: CDF[BinomialDistribution[1e12, 1e-12], 2]
    assert_allclose(binom.cdf(2, 10**12, 10**-12), 0.91969860292869777384)

