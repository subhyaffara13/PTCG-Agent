
def test_picking_callbacks_overlap(big_on_axes, small_on_axes, click_on):
    """Test pick events on normal, host or parasite axes."""
    # Two rectangles are drawn and "clicked on", a small one and a big one
    # enclosing the small one. The axis on which they are drawn as well as the
    # rectangle that is clicked on are varied.
    # In each case we expect that both rectangles are picked if we click on the
    # small one and only the big one is picked if we click on the big one.
    # Also tests picking on normal axes ("gca") as a control.
    big = plt.Rectangle((0.25, 0.25), 0.5, 0.5, picker=5)
    small = plt.Rectangle((0.4, 0.4), 0.2, 0.2, facecolor="r", picker=5)
    # Machinery for "receiving" events
    received_events = []
    def on_pick(event):
        received_events.append(event)
    plt.gcf().canvas.mpl_connect('pick_event', on_pick)
    # Shortcut
    rectangles_on_axes = (big_on_axes, small_on_axes)
    # Axes setup
    axes = {"gca": None, "host": None, "parasite": None}
    if "gca" in rectangles_on_axes:
        axes["gca"] = plt.gca()
    if "host" in rectangles_on_axes or "parasite" in rectangles_on_axes:
        axes["host"] = host_subplot(111)
        axes["parasite"] = axes["host"].twin()
    # Add rectangles to axes
    axes[big_on_axes].add_patch(big)
    axes[small_on_axes].add_patch(small)
    # Simulate picking with click mouse event
    if click_on == "big":
        click_axes = axes[big_on_axes]
        axes_coords = (0.3, 0.3)
    else:
        click_axes = axes[small_on_axes]
        axes_coords = (0.5, 0.5)
    # In reality mouse events never happen on parasite axes, only host axes
    if click_axes is axes["parasite"]:
        click_axes = axes["host"]
    (x, y) = click_axes.transAxes.transform(axes_coords)
    m = MouseEvent("button_press_event", click_axes.get_figure(root=True).canvas, x, y,
                   button=1)
    click_axes.pick(m)
    # Checks
    expected_n_events = 2 if click_on == "small" else 1
    assert len(received_events) == expected_n_events
    event_rects = [event.artist for event in received_events]
    assert big in event_rects
    if click_on == "small":
        assert small in event_rects

