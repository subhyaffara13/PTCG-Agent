
def test_regression_ticket_1530():
    # Check the starting value works for Cauchy distribution fit.
    rng = np.random.default_rng(654321)
    rvs = stats.cauchy.rvs(size=100, random_state=rng)
    params = stats.cauchy.fit(rvs)
    expected = (0.045, 1.142)
    assert_almost_equal(params, expected, decimal=1)

