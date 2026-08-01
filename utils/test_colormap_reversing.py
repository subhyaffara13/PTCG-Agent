
def test_colormap_reversing(name):
    """
    Check the generated _lut data of a colormap and corresponding reversed
    colormap if they are almost the same.
    """
    cmap = mpl.colormaps[name]
    cmap_r = cmap.reversed()
    if not cmap_r._isinit:
        cmap._init()
        cmap_r._init()
    assert_array_almost_equal(cmap._lut[:-3], cmap_r._lut[-4::-1])
    # Test the bad, over, under values too
    assert_array_almost_equal(cmap(-np.inf), cmap_r(np.inf))
    assert_array_almost_equal(cmap(np.inf), cmap_r(-np.inf))
    assert_array_almost_equal(cmap(np.nan), cmap_r(np.nan))

