
def test_interactive_pan(key, mouseend, expectedxlim, expectedylim):
    fig, ax = plt.subplots()
    ax.plot(np.arange(10))
    assert ax.get_navigate()
    # Set equal aspect ratio to easier see diagonal snap
    ax.set_aspect('equal')

    # Mouse move starts from 0.5, 0.5
    mousestart = (0.5, 0.5)
    # Convert to screen coordinates ("s").  Events are defined only with pixel
    # precision, so round the pixel values, and below, check against the
    # corresponding xdata/ydata, which are close but not equal to d0/d1.
    sstart = ax.transData.transform(mousestart).astype(int)
    send = ax.transData.transform(mouseend).astype(int)

    # Set up the mouse movements
    start_event = MouseEvent(
        "button_press_event", fig.canvas, *sstart, button=MouseButton.LEFT,
        key=key)
    drag_event = MouseEvent(
        "motion_notify_event", fig.canvas, *send, button=MouseButton.LEFT,
        buttons={MouseButton.LEFT}, key=key)
    stop_event = MouseEvent(
        "button_release_event", fig.canvas, *send, button=MouseButton.LEFT,
        key=key)

    tb = NavigationToolbar2(fig.canvas)
    tb.pan()
    tb.press_pan(start_event)
    tb.drag_pan(drag_event)
    tb.release_pan(stop_event)
    # Should be close, but won't be exact due to screen integer resolution
    assert tuple(ax.get_xlim()) == pytest.approx(expectedxlim, abs=0.02)
    assert tuple(ax.get_ylim()) == pytest.approx(expectedylim, abs=0.02)

