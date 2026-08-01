
def test_pan():
    """Test mouse panning using the middle mouse button."""

    def convert_lim(dmin, dmax):
        """Convert min/max limits to center and range."""
        center = (dmin + dmax) / 2
        range_ = dmax - dmin
        return center, range_

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(0, 0, 0)
    fig.canvas.draw()

    x_center0, x_range0 = convert_lim(*ax.get_xlim3d())
    y_center0, y_range0 = convert_lim(*ax.get_ylim3d())
    z_center0, z_range0 = convert_lim(*ax.get_zlim3d())

    # move mouse diagonally to pan along all axis.
    MouseEvent._from_ax_coords(
        "button_press_event", ax, (0, 0), MouseButton.MIDDLE)._process()
    MouseEvent._from_ax_coords(
        "motion_notify_event", ax, (1, 1), MouseButton.MIDDLE)._process()

    x_center, x_range = convert_lim(*ax.get_xlim3d())
    y_center, y_range = convert_lim(*ax.get_ylim3d())
    z_center, z_range = convert_lim(*ax.get_zlim3d())

    # Ranges have not changed
    assert x_range == pytest.approx(x_range0)
    assert y_range == pytest.approx(y_range0)
    assert z_range == pytest.approx(z_range0)

    # But center positions have
    assert x_center != pytest.approx(x_center0)
    assert y_center != pytest.approx(y_center0)
    assert z_center != pytest.approx(z_center0)

