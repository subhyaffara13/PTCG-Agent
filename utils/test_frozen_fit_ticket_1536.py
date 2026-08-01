
def test_frozen_fit_ticket_1536():
    rng = np.random.default_rng(5678)
    true = np.array([0.25, 0., 0.5])
    x = stats.lognorm.rvs(true[0], true[1], true[2], size=100, random_state=rng)

    with np.errstate(divide='ignore'):
        params = np.array(stats.lognorm.fit(x, floc=0.))

    assert_almost_equal(params, true, decimal=2)

    params = np.array(stats.lognorm.fit(x, fscale=0.5, loc=0))
    assert_almost_equal(params, true, decimal=2)

    params = np.array(stats.lognorm.fit(x, f0=0.25, loc=0))
    assert_almost_equal(params, true, decimal=2)

    params = np.array(stats.lognorm.fit(x, f0=0.25, floc=0))
    assert_almost_equal(params, true, decimal=2)

    rng = np.random.default_rng(5678)
    loc = 1
    floc = 0.9
    x = stats.norm.rvs(loc, 2., size=100, random_state=rng)
    params = np.array(stats.norm.fit(x, floc=floc))
    expected = np.array([floc, np.sqrt(((x-floc)**2).mean())])
    assert_almost_equal(params, expected, decimal=4)

