
def test_on_move_vertical_axis(vertical_axis: str) -> None:
    """
    Test vertical axis is respected when rotating the plot interactively.
    """
    ax = plt.subplot(1, 1, 1, projection="3d")
    ax.view_init(elev=0, azim=0, roll=0, vertical_axis=vertical_axis)
    ax.get_figure().canvas.draw()

    proj_before = ax.get_proj()
    MouseEvent._from_ax_coords(
        "button_press_event", ax, (0, 1), MouseButton.LEFT)._process()
    MouseEvent._from_ax_coords(
        "motion_notify_event", ax, (.5, .8), MouseButton.LEFT)._process()

    assert ax._axis_names.index(vertical_axis) == ax._vertical_axis

    # Make sure plot has actually moved:
    proj_after = ax.get_proj()
    np.testing.assert_raises(
        AssertionError, np.testing.assert_allclose, proj_before, proj_after
    )

