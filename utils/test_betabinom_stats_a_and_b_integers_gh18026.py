
def test_betabinom_stats_a_and_b_integers_gh18026(dtypes):
    # gh-18026 reported that `betabinom` kurtosis calculation fails when some
    # parameters are integers. Check that this is resolved.
    n_type, a_type, b_type = dtypes
    n, a, b = n_type(10), a_type(2), b_type(3)
    assert_allclose(betabinom.stats(n, a, b, moments='k'), -0.6904761904761907)

