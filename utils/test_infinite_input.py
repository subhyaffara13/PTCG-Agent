
def test_infinite_input():
    assert_almost_equal(stats.skellam.sf(np.inf, 10, 11), 0)
    assert_almost_equal(stats.ncx2._cdf(np.inf, 8, 0.1), 1)

