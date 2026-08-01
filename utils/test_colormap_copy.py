
def test_colormap_copy():
    cmap = plt.colormaps["Reds"]
    copied_cmap = copy.copy(cmap)
    with np.errstate(invalid='ignore'):
        ret1 = copied_cmap([-1, 0, .5, 1, np.nan, np.inf])
    cmap2 = copy.copy(copied_cmap)
    with pytest.warns(PendingDeprecationWarning):
        cmap2.set_bad('g')
    with np.errstate(invalid='ignore'):
        ret2 = copied_cmap([-1, 0, .5, 1, np.nan, np.inf])
    assert_array_equal(ret1, ret2)
    # again with the .copy method:
    cmap = plt.colormaps["Reds"]
    copied_cmap = cmap.copy()
    with np.errstate(invalid='ignore'):
        ret1 = copied_cmap([-1, 0, .5, 1, np.nan, np.inf])
    cmap2 = copy.copy(copied_cmap)
    with pytest.warns(PendingDeprecationWarning):
        cmap2.set_bad('g')
    with np.errstate(invalid='ignore'):
        ret2 = copied_cmap([-1, 0, .5, 1, np.nan, np.inf])
    assert_array_equal(ret1, ret2)

