
def test_rank_filter_noninteger_rank(xp):
    # regression test for issue 9388: ValueError for
    # non integer rank when performing rank_filter
    arr = xp.asarray(np.random.random((10, 20, 30)))
    footprint = xp.asarray(np.ones((1, 1, 10), dtype=bool))
    assert_raises(TypeError, ndimage.rank_filter, arr, 0.5,
                  footprint=footprint)

