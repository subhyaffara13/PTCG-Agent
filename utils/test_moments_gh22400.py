
def test_moments_gh22400():
    # Regression test for gh-22400
    # Check for correct results at c=0 with no warnings. While we're at it,
    # check that NaN and sufficiently negative input produce NaNs, and output
    # with `c=1` also agrees with reference values.
    res = np.asarray(stats.genextreme.stats([0.0, np.nan, 1, -1.5], moments='mvsk'))

    # Reference values for c=0 (Wikipedia)
    mean = np.euler_gamma
    var = np.pi**2 / 6
    skew = 12 * np.sqrt(6) * special.zeta(3) / np.pi**3
    kurt = 12 / 5
    ref_0 = [mean, var, skew, kurt]
    ref_1 = ref_3 = [np.nan]*4
    ref_2 = [0, 1, -2, 6]  # Wolfram Alpha, MaxStableDistribution[0, 1, -1]

    assert_allclose(res[:, 0], ref_0, rtol=1e-14)
    assert_equal(res[:, 1], ref_1)
    assert_allclose(res[:, 2], ref_2, rtol=1e-14)
    assert_equal(res[:, 3], ref_3)

