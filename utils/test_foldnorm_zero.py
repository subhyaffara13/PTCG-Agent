
def test_foldnorm_zero():
    # Parameter value c=0 was not enabled, see gh-2399.
    rv = stats.foldnorm(0, scale=1)
    assert_equal(rv.cdf(0), 0)  # rv.cdf(0) previously resulted in: nan

