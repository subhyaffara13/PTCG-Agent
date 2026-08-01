
def test_ctrl_rotation_snaps_to_5deg():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    initial = (12.3, 33.7, 2.2)
    ax.view_init(*initial)
    fig.canvas.draw()

    s = 0.25
    step = plt.rcParams["axes3d.snap_rotation"]

    # First rotation without Ctrl
    with mpl.rc_context({'axes3d.mouserotationstyle': 'azel'}):
        MouseEvent._from_ax_coords(
            "button_press_event", ax, (0, 0), MouseButton.LEFT
        )._process()

        MouseEvent._from_ax_coords(
            "motion_notify_event",
            ax,
            (s * ax._pseudo_w, s * ax._pseudo_h),
            MouseButton.LEFT,
        )._process()

    fig.canvas.draw()

    rotated_elev = ax.elev
    rotated_azim = ax.azim
    rotated_roll = ax.roll

    # Reset before ctrl rotation
    ax.view_init(*initial)
    fig.canvas.draw()

    # Now rotate with Ctrl
    with mpl.rc_context({'axes3d.mouserotationstyle': 'azel'}):
        MouseEvent._from_ax_coords(
            "button_press_event", ax, (0, 0), MouseButton.LEFT
        )._process()

        MouseEvent._from_ax_coords(
            "motion_notify_event",
            ax,
            (s * ax._pseudo_w, s * ax._pseudo_h),
            MouseButton.LEFT,
            key="control"
        )._process()

    fig.canvas.draw()

    expected_elev = step * round(rotated_elev / step)
    expected_azim = step * round(rotated_azim / step)
    expected_roll = step * round(rotated_roll / step)

    assert ax.elev == pytest.approx(expected_elev)
    assert ax.azim == pytest.approx(expected_azim)
    assert ax.roll == pytest.approx(expected_roll)

    plt.close(fig)

