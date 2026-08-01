
def test_grid_axes_position(direction):
    """Test positioning of the axes in Grid."""
    fig = plt.figure()
    grid = Grid(fig, 111, (2, 2), direction=direction)
    loc = [ax.get_axes_locator() for ax in np.ravel(grid.axes_row)]
    # Test nx.
    assert loc[1].args[0] > loc[0].args[0]
    assert loc[0].args[0] == loc[2].args[0]
    assert loc[3].args[0] == loc[1].args[0]
    # Test ny.
    assert loc[2].args[1] < loc[0].args[1]
    assert loc[0].args[1] == loc[1].args[1]
    assert loc[3].args[1] == loc[2].args[1]

