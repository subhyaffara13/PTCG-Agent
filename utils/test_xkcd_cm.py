
def test_xkcd_cm():
    assert mpl.rcParams["path.sketch"] is None
    with plt.xkcd():
        assert mpl.rcParams["path.sketch"] == (1, 100, 2)
    assert mpl.rcParams["path.sketch"] is None

