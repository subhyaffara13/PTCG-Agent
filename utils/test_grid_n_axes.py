
def test_grid_n_axes():
    fig = plt.figure()
    grid = Grid(fig, 111, (3, 3), n_axes=5)
    assert len(fig.axes) == grid.n_axes == 5
    with pytest.warns(mpl.MatplotlibDeprecationWarning, match="ngrids attribute"):
        assert grid.ngrids == 5

