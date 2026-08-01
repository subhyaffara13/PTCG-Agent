
def test_grid_axes_lists():
    """Test Grid axes_all, axes_row and axes_column relationship."""
    fig = plt.figure()
    grid = Grid(fig, 111, (2, 3), direction="row")
    assert_array_equal(grid, grid.axes_all)
    assert_array_equal(grid.axes_row, np.transpose(grid.axes_column))
    assert_array_equal(grid, np.ravel(grid.axes_row), "row")
    assert grid.get_geometry() == (2, 3)
    grid = Grid(fig, 111, (2, 3), direction="column")
    assert_array_equal(grid, np.ravel(grid.axes_column), "column")

