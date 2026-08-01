
def assert_plots_equal(ax1, ax2, labels=True):

    assert_artists_equal(ax1.patches, ax2.patches)
    assert_artists_equal(ax1.lines, ax2.lines)
    assert_artists_equal(ax1.collections, ax2.collections)

    if labels:
        assert ax1.get_xlabel() == ax2.get_xlabel()
        assert ax1.get_ylabel() == ax2.get_ylabel()

