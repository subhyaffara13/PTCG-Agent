
def test_plotting_positions():
    # Regression test for #1256
    pos = mstats.plotting_positions(np.arange(3), 0, 0)
    assert_array_almost_equal(pos.data, np.array([0.25, 0.5, 0.75]))

