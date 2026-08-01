
def test_rvs_gh2069_regression():
    # Regression tests for gh-2069.  In scipy 0.17 and earlier,
    # these tests would fail.
    #
    # A typical example of the broken behavior:
    # >>> norm.rvs(loc=np.zeros(5), scale=np.ones(5))
    # array([-2.49613705, -2.49613705, -2.49613705, -2.49613705, -2.49613705])
    rng = np.random.RandomState(123)
    vals = stats.norm.rvs(loc=np.zeros(5), scale=1, random_state=rng)
    d = np.diff(vals)
    npt.assert_(np.all(d != 0), "All the values are equal, but they shouldn't be!")
    vals = stats.norm.rvs(loc=0, scale=np.ones(5), random_state=rng)
    d = np.diff(vals)
    npt.assert_(np.all(d != 0), "All the values are equal, but they shouldn't be!")
    vals = stats.norm.rvs(loc=np.zeros(5), scale=np.ones(5), random_state=rng)
    d = np.diff(vals)
    npt.assert_(np.all(d != 0), "All the values are equal, but they shouldn't be!")
    vals = stats.norm.rvs(loc=np.array([[0], [0]]), scale=np.ones(5),
                          random_state=rng)
    d = np.diff(vals.ravel())
    npt.assert_(np.all(d != 0), "All the values are equal, but they shouldn't be!")

    assert_raises(ValueError, stats.norm.rvs, [[0, 0], [0, 0]],
                  [[1, 1], [1, 1]], 1)
    assert_raises(ValueError, stats.gamma.rvs, [2, 3, 4, 5], 0, 1, (2, 2))
    assert_raises(ValueError, stats.gamma.rvs, [1, 1, 1, 1], [0, 0, 0, 0],
                  [[1], [2]], (4,))

