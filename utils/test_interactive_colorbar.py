
def test_interactive_colorbar(plot_func, orientation, tool, button, expected):
    fig, ax = plt.subplots()
    data = np.arange(12).reshape((4, 3))
    vmin0, vmax0 = 0, 10
    coll = getattr(ax, plot_func)(data, vmin=vmin0, vmax=vmax0)

    cb = fig.colorbar(coll, ax=ax, orientation=orientation)
    if plot_func == "contourf":
        # Just determine we can't navigate and exit out of the test
        assert not cb.ax.get_navigate()
        return

    assert cb.ax.get_navigate()

    # Mouse from 4 to 6 (data coordinates, "d").
    vmin, vmax = 4, 6
    # The y coordinate doesn't matter, it just needs to be between 0 and 1
    # However, we will set d0/d1 to the same y coordinate to test that small
    # pixel changes in that coordinate doesn't cancel the zoom like a normal
    # axes would.
    d0 = (vmin, 0.5)
    d1 = (vmax, 0.5)
    # Swap them if the orientation is vertical
    if orientation == "vertical":
        d0 = d0[::-1]
        d1 = d1[::-1]
    # Convert to screen coordinates ("s").  Events are defined only with pixel
    # precision, so round the pixel values, and below, check against the
    # corresponding xdata/ydata, which are close but not equal to d0/d1.
    s0 = cb.ax.transData.transform(d0).astype(int)
    s1 = cb.ax.transData.transform(d1).astype(int)

    # Set up the mouse movements
    start_event = MouseEvent(
        "button_press_event", fig.canvas, *s0, button)
    drag_event = MouseEvent(
        "motion_notify_event", fig.canvas, *s1, button, buttons={button})
    stop_event = MouseEvent(
        "button_release_event", fig.canvas, *s1, button)

    tb = NavigationToolbar2(fig.canvas)
    if tool == "zoom":
        tb.zoom()
        tb.press_zoom(start_event)
        tb.drag_zoom(drag_event)
        tb.release_zoom(stop_event)
    else:
        tb.pan()
        tb.press_pan(start_event)
        tb.drag_pan(drag_event)
        tb.release_pan(stop_event)

    # Should be close, but won't be exact due to screen integer resolution
    assert (cb.vmin, cb.vmax) == pytest.approx(expected, abs=0.15)

