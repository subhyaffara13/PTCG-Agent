
def test_view_init_vertical_axis(
    vertical_axis, proj_expected, axis_lines_expected, tickdirs_expected
):
    """
    Test the actual projection, axis lines and ticks matches expected values.

    Parameters
    ----------
    vertical_axis : str
        Axis to align vertically.
    proj_expected : ndarray
        Expected values from ax.get_proj().
    axis_lines_expected : tuple of arrays
        Edgepoints of the axis line. Expected values retrieved according
        to ``ax.get_[xyz]axis().line.get_data()``.
    tickdirs_expected : list of int
        indexes indicating which axis to create a tick line along.
    """
    rtol = 2e-06
    ax = plt.subplot(1, 1, 1, projection="3d")
    ax.view_init(elev=0, azim=0, roll=0, vertical_axis=vertical_axis)
    ax.get_figure().canvas.draw()

    # Assert the projection matrix:
    proj_actual = ax.get_proj()
    np.testing.assert_allclose(proj_expected, proj_actual, rtol=rtol)

    for i, axis in enumerate([ax.get_xaxis(), ax.get_yaxis(), ax.get_zaxis()]):
        # Assert black lines are correctly aligned:
        axis_line_expected = axis_lines_expected[i]
        axis_line_actual = axis.line.get_data()
        np.testing.assert_allclose(axis_line_expected, axis_line_actual,
                                   rtol=rtol)

        # Assert ticks are correctly aligned:
        tickdir_expected = tickdirs_expected[i]
        tickdir_actual = axis._get_tickdir('default')
        np.testing.assert_array_equal(tickdir_expected, tickdir_actual)

