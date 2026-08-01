
def test_interactive_zoom():
    fig, ax = plt.subplots()
    ax.set(xscale="logit")
    assert ax.get_navigate_mode() is None

    tb = NavigationToolbar2(fig.canvas)
    tb.zoom()
    assert ax.get_navigate_mode() == 'ZOOM'

    xlim0 = ax.get_xlim()
    ylim0 = ax.get_ylim()

    # Zoom from x=1e-6, y=0.1 to x=1-1e-5, 0.8 (data coordinates, "d").
    d0 = (1e-6, 0.1)
    d1 = (1-1e-5, 0.8)
    # Convert to screen coordinates ("s").  Events are defined only with pixel
    # precision, so round the pixel values, and below, check against the
    # corresponding xdata/ydata, which are close but not equal to d0/d1.
    s0 = ax.transData.transform(d0).astype(int)
    s1 = ax.transData.transform(d1).astype(int)

    # Zoom in.
    start_event = MouseEvent(
        "button_press_event", fig.canvas, *s0, MouseButton.LEFT)
    fig.canvas.callbacks.process(start_event.name, start_event)
    stop_event = MouseEvent(
        "button_release_event", fig.canvas, *s1, MouseButton.LEFT)
    fig.canvas.callbacks.process(stop_event.name, stop_event)
    assert ax.get_xlim() == (start_event.xdata, stop_event.xdata)
    assert ax.get_ylim() == (start_event.ydata, stop_event.ydata)

    # Zoom out.
    start_event = MouseEvent(
        "button_press_event", fig.canvas, *s1, MouseButton.RIGHT)
    fig.canvas.callbacks.process(start_event.name, start_event)
    stop_event = MouseEvent(
        "button_release_event", fig.canvas, *s0, MouseButton.RIGHT)
    fig.canvas.callbacks.process(stop_event.name, stop_event)
    # Absolute tolerance much less than original xmin (1e-7).
    assert ax.get_xlim() == pytest.approx(xlim0, rel=0, abs=1e-10)
    assert ax.get_ylim() == pytest.approx(ylim0, rel=0, abs=1e-10)

    tb.zoom()
    assert ax.get_navigate_mode() is None

    assert not ax.get_autoscalex_on() and not ax.get_autoscaley_on()

