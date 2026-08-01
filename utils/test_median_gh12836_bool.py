
def test_median_gh12836_bool(xp):
    # test boolean addition fix on example from gh-12836
    a = np.asarray([1, 1], dtype=bool)
    a = xp.asarray(a)
    output = ndimage.median(a, labels=xp.ones((2,)), index=xp.asarray([1]))
    assert_array_almost_equal(output, xp.asarray([1.0]))

