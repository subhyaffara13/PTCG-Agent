
def test_axis_None_vs_tuple_with_broadcasting():
    # `axis` `None` should be equivalent to tuple with all axes,
    # which should be equivalent to raveling the arrays before passing them
    rng = np.random.default_rng(0)
    x = rng.random((5, 1))
    y = rng.random((1, 5))
    x2, y2 = np.broadcast_arrays(x, y)

    res0 = stats.mannwhitneyu(x.ravel(), y.ravel())
    res1 = stats.mannwhitneyu(x, y, axis=None)
    res2 = stats.mannwhitneyu(x, y, axis=(0, 1))
    res3 = stats.mannwhitneyu(x2.ravel(), y2.ravel())

    assert res1 == res0
    assert res2 == res0
    assert res3 != res0

