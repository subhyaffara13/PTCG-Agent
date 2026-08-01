
def test_span_selector_animated_artists_callback():
    """Check that the animated artists changed in callbacks are updated."""
    x = np.linspace(0, 2 * np.pi, 100)
    values = np.sin(x)

    fig, ax = plt.subplots()
    ln, = ax.plot(x, values, animated=True)
    ln2, = ax.plot([], animated=True)

    # spin the event loop to let the backend process any pending operations
    # before drawing artists
    # See blitting tutorial
    plt.pause(0.1)
    ax.draw_artist(ln)
    fig.canvas.blit(fig.bbox)

    def mean(vmin, vmax):
        # Return mean of values in x between *vmin* and *vmax*
        indmin, indmax = np.searchsorted(x, (vmin, vmax))
        v = values[indmin:indmax].mean()
        ln2.set_data(x, np.full_like(x, v))

    span = widgets.SpanSelector(ax, mean, direction='horizontal',
                                onmove_callback=mean,
                                interactive=True,
                                drag_from_anywhere=True,
                                useblit=True)

    # Add span selector and check that the line is draw after it was updated
    # by the callback
    MouseEvent._from_ax_coords("button_press_event", ax, (1, 2), 1)._process()
    MouseEvent._from_ax_coords("motion_notify_event", ax, (2, 2), 1)._process()
    assert span._get_animated_artists() == (ln, ln2)
    assert ln.stale is False
    assert ln2.stale
    assert_allclose(ln2.get_ydata(), 0.9547335049088455)
    span.update()
    assert ln2.stale is False

    # Change span selector and check that the line is drawn/updated after its
    # value was updated by the callback
    MouseEvent._from_ax_coords("button_press_event", ax, (4, 0), 1)._process()
    MouseEvent._from_ax_coords("motion_notify_event", ax, (5, 2), 1)._process()
    assert ln.stale is False
    assert ln2.stale
    assert_allclose(ln2.get_ydata(), -0.9424150707548072)
    MouseEvent._from_ax_coords("button_release_event", ax, (5, 2), 1)._process()
    assert ln2.stale is False

