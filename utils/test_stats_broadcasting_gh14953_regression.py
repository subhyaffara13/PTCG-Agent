
def test_stats_broadcasting_gh14953_regression():
    # test case in gh14953
    loc = [0., 0.]
    scale = [[1.], [2.], [3.]]
    assert_equal(stats.norm.var(loc, scale), [[1., 1.], [4., 4.], [9., 9.]])
    # test some edge cases
    loc = np.empty((0, ))
    scale = np.empty((1, 0))
    assert stats.norm.var(loc, scale).shape == (1, 0)

