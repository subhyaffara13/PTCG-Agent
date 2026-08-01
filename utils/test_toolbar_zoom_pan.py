
def test_toolbar_zoom_pan(tool, button, key, expected):
    # NOTE: The expected zoom values are rough ballparks of moving in the view
    #       to make sure we are getting the right direction of motion.
    #       The specific values can and should change if the zoom movement
    #       scaling factor gets updated.
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(0, 0, 0)
    fig.canvas.draw()
    xlim0, ylim0, zlim0 = ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()

    # Mouse from (0, 0) to (1, 1)
    d0 = (0, 0)
    d1 = (1, 1)
    # Convert to screen coordinates ("s").  Events are defined only with pixel
    # precision, so round the pixel values, and below, check against the
    # corresponding xdata/ydata, which are close but not equal to d0/d1.
    s0 = ax.transData.transform(d0).astype(int)
    s1 = ax.transData.transform(d1).astype(int)

    # Set up the mouse movements
    start_event = MouseEvent(
        "button_press_event", fig.canvas, *s0, button, key=key)
    drag_event = MouseEvent(
        "motion_notify_event", fig.canvas, *s1, button, key=key, buttons={button})
    stop_event = MouseEvent(
        "button_release_event", fig.canvas, *s1, button, key=key)

    tb = NavigationToolbar2(fig.canvas)
    if tool == "zoom":
        tb.zoom()
    else:
        tb.pan()

    start_event._process()
    drag_event._process()
    stop_event._process()

    # Should be close, but won't be exact due to screen integer resolution
    xlim, ylim, zlim = expected
    assert ax.get_xlim3d() == pytest.approx(xlim, abs=0.01)
    assert ax.get_ylim3d() == pytest.approx(ylim, abs=0.01)
    assert ax.get_zlim3d() == pytest.approx(zlim, abs=0.01)

    # Ensure that back, forward, and home buttons work
    tb.back()
    assert ax.get_xlim3d() == pytest.approx(xlim0)
    assert ax.get_ylim3d() == pytest.approx(ylim0)
    assert ax.get_zlim3d() == pytest.approx(zlim0)

    tb.forward()
    assert ax.get_xlim3d() == pytest.approx(xlim, abs=0.01)
    assert ax.get_ylim3d() == pytest.approx(ylim, abs=0.01)
    assert ax.get_zlim3d() == pytest.approx(zlim, abs=0.01)

    tb.home()
    assert ax.get_xlim3d() == pytest.approx(xlim0)
    assert ax.get_ylim3d() == pytest.approx(ylim0)
    assert ax.get_zlim3d() == pytest.approx(zlim0)

